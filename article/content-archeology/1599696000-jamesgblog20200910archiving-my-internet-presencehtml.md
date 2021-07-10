---
author:
    name: James Gallagher
    url: https://jamesg.blog
date: '2020-09-10T00:00:00+00:00'
source: https://jamesg.blog/2020/09/10/archiving-my-internet-presence.html
target: https://petermolnar.net/article/content-archeology/index.html
type: link

---

<p>I am working my way through reading a blog post by Peter Molnar where he talks about his project to <a href="https://petermolnar.net/article/content-archeology/index.html">retrieve his old websites</a>. <a href="https://jamesg.blog/2020/09/10/archiving-my-internet-presence.html#fn:1">1</a> Reading through this post has me thinking, again, about how I can archive my internet presence.</p>

<p>Content on the internet is fleeting. This became real to me when I started to think about all of the websites I have hosted in the past. My website that I hosted on Carrd for a number of months a few years ago is now lost to time. I did not archive the site on the Wayback Machine and I deleted my Carrd account because I was no longer using it. Part of my internet history is gone.</p>

<p>I am not distressed by losing this one piece of information about my history. Although my Carrd site was really the first professional website I had, it was only one page. I did not have much content aside from a brief description of who I was. This site is a different story.</p>

<h2>Storing Content in Files</h2>

<p>There is a debate in the IndieWeb community about the so-called database antipattern. The idea is that databases introduce a lot of complexity and overhead into a project. This is called a “DBA tax,” or a database administration tax. I have found myself choosing a position on this debate, which is rare because I usually like to stay neutral on controversial topics. I believe that I need to store my content in files.</p>

<p>I evaluated many factors when I decided to stick with this static website which is built using Jekyll. One of these factors was that I wanted my data to be easily accessible to me and to anyone else who wants to read it. Storing data in files makes my writing and content much easier to access and modify. Bringing in a database would only put my content somewhere that I cannot really see it. I can see the results from a database query but it is not the same as having a file that backs the content. <a href="https://jamesg.blog/2020/09/10/archiving-my-internet-presence.html#fn:2">2</a></p>

<p>On this website, all of my content is stored in files. I have the static output for my site which is complete and ready to deploy. That is the version that my visitors see. It’s also significant that Jekyll stores all its data in files. I don’t even have to build my site to read its contents. I can see the structure. Every piece of information is in a file. I can go to my old blog posts and read through the front matter to understand what attributes are associated with the post. My post is in markdown so it is easy to read even without an editor.</p>

<p>Storing as much of my data in files as possible is probably the best shot I have at keeping my online presence archived for longer.</p>

<h2>My GitHub</h2>

<p>I have considered mirroring all my code to sourcehut twice or maybe three times this year. In all these cases, I’ve done quite a bit of research about mirroring repositories. The first iteration was a project where I just uploaded all my repositories after I run a script. The second project was more elegant and mirrored each commit to a repository as soon as the commit was created.</p>

<p>I now think this is unnecessary. This is taking my backup system too far. Git in itself has everything that I need. I often forget that Git in itself is an archiving system. It’s purpose is to create a record of how a project has evolved. So, instead of worrying about creating a mirror of my code, I am taking faith in the fact that Git will help keep my code archived for longer.</p>

<p>Even if the Git standard is not around in the future, at the very least the files that I have stored will still be accessible. By Git, I don’t just mean GitHub. I have a local copy of my blog on my computer. If my GitHub repository suddenly becomes unavailable, I do have a backup locally. Now that I write this I do wonder whether two backups is enough. Maybe I am trying to engineer a solution to a problem that is not really a problem for me.</p>

<h2>The Internet Archive</h2>

<p>I wrote a quick script a few days ago that uploaded my entire blog to the Internet Archive. It was the first entry under my new domain, jamesg.blog. I hope that it will be the first of many. The Internet Archive is fully independent from me. I cannot control its contents, other than submitting new files. This means that I will always have a dependable backup that I do not need to worry about maintaining. This is significant because I have found that it is the easiest systems to use that last the longest. If I had to manage yet another backup, I’d probably forget about it. <a href="https://jamesg.blog/2020/09/10/archiving-my-internet-presence.html#fn:3">3</a></p>

<p>The Internet Archive has bits and pieces from my internet history but it’s hardly a comprehensive archive. I have to initiate archives myself. I haven’t really thought about this until now. I’ve always taken for granted that content on the internet is <em>just there.</em> I just need to navigate to a URL. I haven’t yet been affected by a major project or site going down that I loved (at least that I am aware of right now) but I do feel like it is only a matter of time. I don’t want that to happen to my internet content.</p>

<h2>My Writing</h2>

<p>Books have lasted the test of time. Some books in libraries are hundreds of years old. What about the internet? Content seems to go away so quickly. I know this because I change my website a lot and there’s already a lot that is lost to history. My WordPress and Squarespace sites from last year are largely gone. I am unsure whether I still have an accessible backup.</p>

<p>When I add content to this site, I want to ask myself whether I can see it existing in the long-term. That is what has discouraged me from adding a <em>Notes</em> section to this site. It would be cool to share short notes on this site. It would also be a lot of overhead. I am researching workflows like a Jekyll and GitHub micropub endpoint but maybe that is a step too far. Maybe, to make my content last the longest, I just need to keep my systems simple.</p>


  <ol><li>
      <p>I highly recommend Peter’s blog, especially for thoughts on technology. Check out the “IT” section for his tech-related writing. <a href="https://jamesg.blog/2020/09/10/archiving-my-internet-presence.html#fnref:1">↩</a></p>
    </li>
    <li>
      <p>I know that you could have a database that stores the locations of data in files. That is another layer of abstraction and complexity that I would have to worry about by using a dynamic site. <a href="https://jamesg.blog/2020/09/10/archiving-my-internet-presence.html#fnref:2">↩</a></p>
    </li>
    <li>
      <p>I am probably going to forget to archive my site, but I am trying. I’m thinking of setting up a cron script on a server to do this for me. I could do it on my Raspberry Pi. Now, there is an interesting idea. <a href="https://jamesg.blog/2020/09/10/archiving-my-internet-presence.html#fnref:3">↩</a></p>
    </li>
  </ol>
