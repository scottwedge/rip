from pathlib import Path
from typing import List
import json
import os
import subprocess
import sys

def requirements_check():
    requirements_not_met = False
    try:
        result = subprocess.run(['dvd_info', '--version'], capture_output=True, text=True)
    except FileNotFoundError:
        print("ERROR, dependency not found: This program requires the 'dvd_info' binary to be in the PATH.")
        requirements_not_met = True
    try:
        result = subprocess.run(['HandBrakeCLI', '--version'], capture_output=True, text=True)
    except FileNotFoundError:
        print("ERROR, dependency not found: This program requires the 'HandBrakeCLI' binary to be in the PATH.")
        requirements_not_met = True
    if requirements_not_met:
        print("\nRequirements not met, exiting.\n")
        sys.exit(1)


def print_title_and_chapter_info(dvd_info, only_title=None, show_chapters=True):
    for title_index, title in enumerate(dvd_info['tracks']):
        if only_title and str(title['track']) != only_title:
            continue
        print(f"Title {title['track']} ({title['length']})")
        if show_chapters:
            for chapter_index, chapter in enumerate(dvd_info['tracks'][title_index]['chapters']):
                print(f"\tChapter {chapter['chapter']} ({chapter['length']})")

def create_ripping_guide(dvd_info, multi_feature_disc=False):
    # Here is a visual of the structure we are building.
    guide = {
        'disc_id': dvd_info['dvd']['dvdread id'],
        # Both types -- Movie or TV -- will have a title.
        'title': '',
        # TV shows will have one or more episodes per disc
        # 'episodes': [
        #     {
        #         'season': '',
        #         'episode': '',
        #         'filename': '',
        #         'title': '',
        #         'chapters': '',
        #     },
        # ],
        # Movies will have one or more features per disc
        # It is rare that a disc has multiple features, but has been observed.
        # 'features': [
        #     {
        #         'feature_title': '',
        #         'filename': '',
        #         'title': '',
        #         'chapters': '',
        #     },
        # ]
    }
    def ask_movie_or_tv() -> str:
        print('Is this a:')
        print('\n1) Movie')
        print('2) Series\n')
        response = input('-> ')
        if response == '1':
            return 'movie'
        elif response == '2':
            return 'tv'
        else:
            print('\nInvalid response.\n')
            return ask_movie_or_tv()

    def ask_tv_title() -> str:
        return input('Series Title: ').strip()

    def ask_movie_title() -> str:
        return input('Movie Title: ').strip()

    def ask_disc_title() -> str:
        return input('Disc Title: ').strip()

    def ask_season() -> str:
        return input('Season #: ').strip().zfill(2)

    def ask_episodes() -> List[str]:
        response = input('Episode #s comma separated (ex: "1,2,3,4,5"): ').strip().replace(' ', '')
        episodes = [number.zfill(2) for number in sorted(list(set(response.split(','))))]
        return episodes

    if multi_feature_disc:
        is_tv = False
    else:
        is_tv = ask_movie_or_tv() == 'tv'
    
    if is_tv:
        title = ask_tv_title()
        guide['title'] = title
        season = ask_season()
        episode_numbers = ask_episodes()
        guide['episodes'] = []
        for episode_number in sorted(episode_numbers):
            print_title_and_chapter_info(dvd_info, show_chapters=False)
            disc_title = input(f'What title of the disc contains episode {episode_number}? ')
            print_title_and_chapter_info(dvd_info, only_title=disc_title)
            disc_chapters = input(f'Which chapters of title {disc_title} make up episode {episode_number}? (example: 1-5) ')
            episode = {
                'season': season,
                'episode': episode_number,
                'filename': f'{title}.S{season}.E{episode_number}.m4v',
                'title': disc_title,
                'chapters': disc_chapters
            }
            guide['episodes'].append(episode)
    else:
        if multi_feature_disc:
            title = ask_disc_title()
        else:
            title = ask_movie_title()
        guide['title'] = title
        guide['features'] = []
        all_features_collected = False
        while not all_features_collected:
            if multi_feature_disc:
                feature_title = ask_movie_title()
            else:
                feature_title = title
            print_title_and_chapter_info(dvd_info, show_chapters=False)
            disc_title = input(f'What title of the disc contains the feature? ')
            print_title_and_chapter_info(dvd_info, only_title=disc_title)
            disc_chapters = input(f'Which chapters of title {disc_title} make up the feature? (example: 1-5) ')
            guide['features'].append({
                'feature_title': feature_title,
                'filename': f'{feature_title}.m4v',
                'title': disc_title,
                'chapters': disc_chapters,
            })
            if multi_feature_disc:
                all_features_collected = not (input('\nDoes this disc have another feature? [y/n]').lower() == 'y')
            else:
                all_features_collected = True
    return guide

def handbrake(drive_path, title, chapters, filename, preset='Fast 480p30'):
    handbrake_process_arguments = [
        'HandBrakeCLI',
        '--preset', preset,
        '--decomb',
        '--markers',
        '--encoder', 'x264',
        '--title', title,
        '--chapters', chapters,
        '-i', drive_path,
        '-o', filename
    ]
    print(f'\n\nNow ripping: {filename}\n\n')
    subprocess.run(handbrake_process_arguments, text=True)

def rip_from(ripping_guide, drive_path):
    if 'episodes' in ripping_guide:
        dvd_rip_dir = f"{Path.home()}/dvd_rips/{ripping_guide['title']}"
        Path(dvd_rip_dir).mkdir(parents=True, exist_ok=True)
        for episode in ripping_guide['episodes']:
            Path(f"{dvd_rip_dir}/Season {episode['season']}").mkdir(parents=True, exist_ok=True)
            handbrake(drive_path, episode['title'], episode['chapters'], f"{dvd_rip_dir}/Season {episode['season']}/{episode['filename']}")
    if 'features' in ripping_guide:
        for feature in ripping_guide['features']:
            dvd_rip_dir = f"{Path.home()}/dvd_rips/{feature['feature_title']}"
            Path(dvd_rip_dir).mkdir(parents=True, exist_ok=True)
            handbrake(drive_path, feature['title'], feature['chapters'], f"{dvd_rip_dir}/{feature['filename']}")
    print('\n\nRipping Complete\n\n')

DRIVE_PATH_CANDIDATES = ['/dev/rdisk2', '/dev/disk1', '/dev/disk2', '/dev/sr0', '/dev/sr1', '/dev/rdisk0', '/dev/rdisk1']

def main():
    title = """

@@@@@@@            @@@           @@@@@@@   
@@@@@@@@           @@@           @@@@@@@@  
@@!  @@@           @@!           @@!  @@@  
!@!  @!@           !@!           !@!  @!@  
@!@!!@!            !!@           @!@@!@!   
!!@!@!             !!!           !!@!!!    
!!: :!!            !!:           !!:       
:!:  !:!           :!:           :!:       
::   :::            ::            ::       
 :   : :           :              :        
                                           
    """
    print(title)
    requirements_check()

    multi_feature_disc = os.getenv('MULTI_FEATURE_DISC', default='false').lower() == 'true'

    dvd_info = None
    drive_path = None
    disc_id = None
    disc_title = None

    for drive_path_candidate in DRIVE_PATH_CANDIDATES:
        result = subprocess.run(['dvd_info', '--json', drive_path_candidate], capture_output=True, text=True)
        if result.stdout and not result.stderr:
            drive_path = drive_path_candidate
            dvd_info_output = result.stdout
            dvd_info_output_json = ''.join([line for line in dvd_info_output.splitlines() if not line.startswith('libdvdread: ')])
            dvd_info = json.loads(dvd_info_output_json)
            disc_id = dvd_info['dvd']['dvdread id']
            disc_title = dvd_info['dvd']['title'] or 'Unknown Title'
            break

    if not drive_path:
        print(f'Could not find disc at any of the following locations: {", ".join(DRIVE_PATH_CANDIDATES)}')
        print('Ensure a disc is inserted, or specify the drive path as an argument.')
        print('Example:')
        print('python3 rip/rip.py /special/disc/path')
        sys.exit(1)
    
    print(f'Found volume "{disc_title}" with id "{disc_id}" at {drive_path}')

    ripping_guide = None

    should_create_ripping_guide = input('\nCreate a ripping guide? [y/n]: ').lower() == 'y'
    if should_create_ripping_guide:
        # create a ripping guide
        ripping_guide = create_ripping_guide(dvd_info, multi_feature_disc)

    rip_from_guide = False
    if ripping_guide:
        print('Please review the ripping guide:\n')
        print(json.dumps(ripping_guide, indent=2))

        ripping_guide_dir = f"{Path.home()}/dvd_ripping_guides"
        Path(ripping_guide_dir).mkdir(parents=True, exist_ok=True)
        ripping_guide_filepath = f"{ripping_guide_dir}/{disc_id}.ripping-guide.json"
        with open(ripping_guide_filepath, "w") as exported_ripping_guide:
            exported_ripping_guide.write(json.dumps(ripping_guide, indent=2))
        rip_from_guide = input('\nRip the disc based on this guide? [y/n]').lower() == 'y'

    if rip_from_guide:
        rip_from(ripping_guide, drive_path)

main()
