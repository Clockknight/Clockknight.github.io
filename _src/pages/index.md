---
title: Projects
class: home
notitle: true
---
<section class="hero">
<p class="eyebrow">{{site.author}}</p>
<h1>{{site.title}}</h1>
<p class="lead">{{site.description}}</p>
</section>

<section class="group">
<h2>Projects</h2>
<p class="group-intro">Projects which I use to help myself automate tasks.</p>
<div class="hub" data-hub data-label="Projects">
<div class="hub-panels">
<article class="hub-item" data-tab="Heirarchy Helper">
<h3><a href="https://github.com/Clockknight/heirarchy-helper">HEIRARCHY HELPER</a></h3>
<p class="summary">A <a href="http://discord.gg">Discord</a> bot that allows you to define relations between roles on your server.</p>
<p>The primary usage of the bot is to enforce a heirarchy between roles.</p>
<p>In this case, heirarchy would mean if you get a "lower" role for whatever reason, the bot will automatically detect the change, and give that user the "higher" role.</p>
</article>
<article class="hub-item" data-tab="Album Downloader">
<h3><a href="https://github.com/Clockknight/album-downloader">ALBUM DOWNLOADER</a></h3>
<p class="summary">Downloads songs based on information available on <a href="http://Discogs.com">Discogs</a>.</p>
<p class="note"><i>Note: While the code itself works, it relies on the pytube library, which does not work as of writing this.</i></p>
<p>Releases is the umbrella term Discogs uses for singles, albums, and eps.</p>
<p>This code stores information about releases that are downloaded, then when the user runs the update option, the code will also download all releases that have yet to be downloaded.</p>
<p>Infomation about the songs are pulled from a json file and used to tag the MP3s as they are downloaded, including album art, album name, and artist name.</p>
</article>
<article class="hub-item" data-tab="Deckbox Exporter">
<h3><a href="https://github.com/Clockknight/deckbox-exporter">DECKBOX EXPORTER</a></h3>
<p class="summary">Takes a .csv from <a href="https://deckbox.org/">Deckbox</a>, and updates your <a href="https://www.tcgplayer.com/">TCGPlayer</a> Seller Inventory to match.</p>
<p>The process has to actually input the values on TCGPlayer's website. I attempted to use TCGPlayer's API to make the process faster, but it did not support manipulating an account's cards available for sale.</p>
<p>Very useful when trying to export your inventory of Magic: The Gathering cards from the Deckbox site to TCGPlayer, if you're looking to sell some of your collection.</p>
</article>
<article class="hub-item" data-tab="GUI Image Sorter">
<h3><a href="https://github.com/Clockknight/gui-image-sorter">GUI IMAGE SORTER</a></h3>
<img src="sorter.png" width="1868" height="750" loading="lazy" alt="Screenshot of the GUI image sorter: an image preview with folder controls alongside">
<p class="summary">Using the TKInter package to create a GUI that allows you to sort images into subdirectories.</p>
<p>Primary purpose of the code is that you can preview images as you put them into different folders, and all folders are relatively accessible, being able to sort them with all controls available on one window regardless of which file you're looking at.</p>
<p>Code is missing some features, which are brought up on the repository's issues page.</p>
</article>
<article class="hub-item" data-tab="Daily Countdown Timer">
<h3><a href="https://github.com/Clockknight/daily-countdown-timer">DAILY COUNTDOWN TIMER</a></h3>
<p class="summary">Code to be a companion to a Rainmeter extension. Resets the extension's timer daily.</p>
<p>Daily Countdown Timer is intended to specifically work with the Rainmeter extension "Magnumizer's Countdown Timer", that will update the date to today, leaving the time untouched.</p>
<p>This program will prompt for a location of thfe timer settings, if it doesn't already have a location saved. It'll save it by putting it to a .txt file in the same directory as the script.</p>
</article>
<article class="hub-item" data-tab="File Raiser">
<h3><a href="https://github.com/Clockknight/file-raiser">FILE RAISER</a></h3>
<p class="summary">File Raiser will recursively search for any files in a directory and its subdirectories, moving them up to the initial directory.</p>
<p>Earliest self-started project. Only script in the list that involves command line arguments.</p>
<p>Also imports pyperclip, since I didn't understand you could just paste things into command line at the time.</p>
</article>
</div>
</div>
</section>

<div class="group-row">
<section class="group">
<h2><a href="https://clockknight.itch.io/">Unity Games</a></h2>
<p class="group-intro">Personal itch.io page. Contains games, mostly in prototype stages or proof of concepts.</p>
<div class="hub" data-hub data-label="Unity Games">
<div class="hub-panels">
<article class="hub-item" data-tab="Chronal Combat">
<h3><a href="https://clockknight.itch.io/chronal-combat">Chronal Combat</a></h3>
<p class="summary">Fighting game. Currently building a prototype.</p>
<p>One of my favorite hobbies is playing fighting games, would love to create one of my own in time.</p>
</article>
<article class="hub-item" data-tab="Speedy Scroller">
<h3><a href="https://clockknight.itch.io/speedy-scroller">Speedy Scroller</a></h3>
<p class="summary">Incremental Game concept.</p>
<p>Built over a week in vacation, trying to get an idea of how scaling should work for these types of games.</p>
</article>
</div>
</div>
</section>

<section class="group">
<h2><a href="https://github.com/EagleJammers">GameJams</a></h2>
<p class="group-intro">Game jams with other EWU students.</p>
<div class="hub" data-hub data-label="GameJams">
<div class="hub-panels">
<article class="hub-item" data-tab="Submissions">
<h3><a href="https://ohhm.itch.io/">Submissions</a></h3>
<p class="summary">Submissions are available on this <a href="https://ohhm.itch.io/">itch.io page</a>.</p>
<p>No submissions I've contributed to have been completed and submitted yet!</p>
</article>
<article class="hub-item" data-tab="EagleJammers">
<h3><a href="https://github.com/EagleJammers">EagleJammers</a></h3>
<p class="summary">I work with other EWU students in a group, participating regularly in the <a href="https://trijam.itch.io/">TriJam Game Jam</a>.</p>
</article>
</div>
</div>
</section>
</div>

<script src="assets/hub.js?v={{hash:assets/hub.js}}" defer></script>
