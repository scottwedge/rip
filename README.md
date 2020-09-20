
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

## CLI disc ripping with repeatability

Setting up a MyLittleCable.Co headend requires a good bit of video content. If
someone is ripping a bunch of DVDs to get TV episodes, they may as well save
the mapping of title/chapters -> season/episode number so that others may
benefit.

This program will (eventually) search for a ripping guide based on the
libdvdread disc id. This would be analogous to a music ripping program filling
in id3 tags from a cddb.

This program (currently) will ask you about the disc in the drive, and request
that you tell it what season it is, what episodes are contained on it, and
finally, for each episode, what the title and chapters are that make up the
episode.

When the program has a ripping guide, either by finding one on the internet or
by you creating one, it will then use it to rip the episodes on the disc,
saving them with filenames and a directory structure based on the show,
season, and episode number.

## Example

Consider the following ripping guide:

```json
{
  "disc_id": "266c6676a30c416bdc6f5f97e7190297",
  "title": "Big Buck Bunny The Animated Series",
  "episodes": [
    {
      "season": "01",
      "episode": "01",
      "filename": "Big Buck Bunny The Animated Series.S01.E01.m4v",
      "title": "1",
      "chapters": "1-5"
    },
    {
      "season": "01",
      "episode": "02",
      "filename": "Big Buck Bunny The Animated Series.S01.E02.m4v",
      "title": "1",
      "chapters": "6-10"
    },
    {
      "season": "01",
      "episode": "03",
      "filename": "Big Buck Bunny The Animated Series.S01.E03.m4v",
      "title": "1",
      "chapters": "11-15"
    },
    {
      "season": "01",
      "episode": "04",
      "filename": "Big Buck Bunny The Animated Series.S01.E04.m4v",
      "title": "1",
      "chapters": "16-20"
    },
    {
      "season": "01",
      "episode": "05",
      "filename": "Big Buck Bunny The Animated Series.S01.E05.m4v",
      "title": "2",
      "chapters": "1-5"
    },
    {
      "season": "01",
      "episode": "06",
      "filename": "Big Buck Bunny The Animated Series.S01.E06.m4v",
      "title": "2",
      "chapters": "6-10"
    },
    {
      "season": "01",
      "episode": "07",
      "filename": "Big Buck Bunny The Animated Series.S01.E07.m4v",
      "title": "2",
      "chapters": "11-15"
    },
    {
      "season": "01",
      "episode": "08",
      "filename": "Big Buck Bunny The Animated Series.S01.E08.m4v",
      "title": "2",
      "chapters": "16-20"
    }
  ]
}
```

This would yield the following file structure:
```
`-- Big Buck Bunny The Animated Series
    `-- Season 01
        |-- Big Buck Bunny The Animated Series.S01.E01.m4v
        |-- Big Buck Bunny The Animated Series.S01.E02.m4v
        |-- Big Buck Bunny The Animated Series.S01.E03.m4v
        |-- Big Buck Bunny The Animated Series.S01.E04.m4v
        |-- Big Buck Bunny The Animated Series.S01.E05.m4v
        |-- Big Buck Bunny The Animated Series.S01.E06.m4v
        |-- Big Buck Bunny The Animated Series.S01.E07.m4v
        `-- Big Buck Bunny The Animated Series.S01.E08.m4v

2 directories, 8 files
```

Ideally, with community contributions, someone would be able to rip their TV
show DVD collection with ease. The only requirement would be to swap discs
when one finishes. Of course, to get there, we need your help! If you create a
ripping guide, please submit it here. In the near future this program will
gain the ability to seek out ripping guides, which will live in the repo
essentially as configuration. We will use homebrew and their formulae as a
model.


## Planned Features

- Look for existing ripping guides and use them if available
- Override HandBrake config with local preferences
- Support DVD bonus features with plex-supported naming conventions


## Installation

- This requires the excellent `dvd_info` tool. See
  https://github.com/beandog/dvd_info for installation instructions.
- This also requires the also excellent `HandBrakeCLI`. See
  https://handbrake.fr/downloads2.php for download links.
- Once you have those tools installed and in the PATH, you should:
  - `git clone git@github.com:My-Little-Cable-Co/rip.git`
  - `cd rip`
  - `python3 rip/rip.py`


## Disclaimer

Don't do anything illegal, now!


## License

MIT License

Copyright (c) 2020 Andrew Duane and MyLittleCable.Co

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
