---
author:
    name: Matthias Pfefferle
    photo: https://webmention.io/avatar/secure.gravatar.com/4937247dd597f4199f42e5d56c8172c2025efeff5209a49bf049b93ea489474d.jpg
    url: https://notiz.blog/author/matthias-pfefferle/
date: '2019-02-21T19:59:18+02:00'
source: https://test.topblogs.de/untitled/
target: https://petermolnar.net/i-want-the-blogs-back/
type: link

---

<p>Die Art wie wir kommunizieren hat sich verändert. Die Flut an Informationen wird immer größer und wir nehmen uns immer weniger Zeit zum lesen und schreiben. Aus E-Mail wurde Messaging, aus Bloggen wurde Microbloggen und wir nutzen Emojis, Hashtags und <a href="https://notiz.blog/2017/10/04/readability/">andere Abkürzungen</a> um die, so schon kurzen Texte, noch weiter zu „optimieren“.</p>



<p>Das ist prinzipiell auch nichts schlimmes, da sich mit jeder neuen Kommunikationsform in der Regel auch das Medium, mit dem ich es konsumiere, ändert. Messaging-Texte lese ich in Telegram und E-Mails kann ich weiterhin in meiner Mail-App lesen.</p>



<p>Komisch wird es aber, wenn sich Medien vermischen, oder wenn Tools versuchen unterschiedliche Medien zu normalisieren. 2011 versuchte Facebook, beispielsweise <a href="https://www.facebook.com/notes/facebook/see-the-messages-that-matter/452288242130">E-Mails und Messaging/Chat zu verheiraten</a> und über eine Oberfläche nutzbar zu machen.</p>



<blockquote>
<p>There are no subject lines, no cc, no bcc, and you can send a message by hitting the Enter key. We modeled it more closely to chat and reduced the number of things you need to do to send a message.</p>
Facebook: <a href="https://www.facebook.com/notes/facebook/see-the-messages-that-matter/452288242130">See the Messages that Matter</a>
</blockquote>



<p>Auf Facebook hat das Vorhaben auch gut funktioniert, aber über die klassiche Mail-App sah ein „Discussion-Thread“ nicht wirklich hübsch aus, weshalb <a href="https://www.theverge.com/2014/2/24/5443454/facebook-retires-its-email-service">das Projekt auch (zum Glück) wieder eingestellt wurde</a>.</p>



<p>Aber wie komme ich auf das Thema?</p>



<p>Aktuell sieht es in meinem Feed-Reader folgendermaßen aus:</p>



<img src="https://notiz.blog/wp-content/uploads/2019/02/reeder-no-titles-feed-576x1024.png" alt="" />Reeder (RSS-Reader) auf dem iPhone



<p>Keine Überschriften, komische Überschriften, nur das Datum oder sogar der ganze Text als Überschrift. Schuld daran ist, die Verschmelzung von Blogging und Microblogging. Oder besser: Die Nutzung eines Feed-Readers um Microblogs zu lesen.</p>



<p><a href="https://micro.blog">Micro.blog</a> ist ein Microblogging-Dienst, der 2017 über eine Kickstarter-Kampangne finanziert wurde. Micro.blog orientiert sich stark an der IndieWeb Community und unterstütz viele IndieWeb Protokolle, wie z.B. Webmentions und Micropub. Der Service unterstützt außerdem das abonnieren von klassischen Blogs wie z.B. WordPress über das gute alte RSS Format. Und hier vermischen sich die beiden Themen.</p>



<p>Aus der <a href="http://help.micro.blog/2018/setting-up-wordpress/#no-titles">WordPress Doku von Micro.blog</a>:</p>



<blockquote><p>Part of indie microblogging is getting back to the simplicity of title-less posts. When you’re writing a microblog post in WordPress, just leave the title blank, and if necessary update the post template to not include the title in HTML or the RSS feed.</p></blockquote>



<p>Durch die IndieWeb Community veröffentlichen viele Personen in meinem Umfeld alle Arten von Texten und anderen Medien auf ihren eigenen Webseiten. Ein signifikanter Anteil von ihnen nutzen dafür WordPress und ein Teil davon wiederum meine Themes. Das heißt ich bin letztendlich sogar dreifach von diesem „Trend“ betroffen: als Konsument, als Entwickler und als Publisher.</p>



<p>Ich verstehe den Ansatz, den Micro.blog verfolgt durchaus:</p>



<blockquote>
<p>You may find that some feed readers don’t gracefully handle posts without titles, often inserting “Untitled” for the title because they expect something to be there. If you see this, the best solution is to email the developer and ask for them to address it. Working around the issue with fake titles — dates, numbers, or portions of the text — will only ensure that client developers never improve their apps to handle title-less posts.</p>
<p></p>
</blockquote>



<p>Apple macht es ganz ähnlich, wenn sie bei neuen iPhones die Kopfhörer-Buchse weg lassen oder bei Laptops nur noch USB-C Anschlüsse verbauen. Man könnte argumentieren, dass es der einzige Weg sei um den Fortschritt voran zu treiben, aber ich bin von den Änderungen meistens eher genervt! Ich bin nämlich derjenige der wieder neue Kopfhörer und einen <strong><em>&amp;%$?§</em></strong> voll Adapter braucht.</p>



<p>Ein ähnliches Gefühl habe ich gerade bei Microblogging über WordPress und Micro.blog. Nicht die RSS-Reader werden gezwungen sich anzupassen, sondern ich muss schauen, wie ich meine Lese- bzw. Schreibgewohnheiten verändere. <a href="https://micro.blog/MrHenko/170619">Ich „muss“ mein Theme anpassen</a>, <a href="https://github.com/pfefferle/wordpress-webmention/issues/166">ich „muss“ meine Schreibgewohnheiten anpassen</a> und ich „muss“ schauen wie ich meinen Feed-Reader wieder „sauber“ bekomme.</p>



<p>Ich würde mir wünschen wenn Micro.blog nicht so restriktiv mit dem Interpretieren von RSS wäre und wenn es einen fließenderen Übergang gäbe.</p>



<p>Ich würde mich freuen, wenn ich weiterhin Titel schreiben dürfte, denn Titel sind gut für den Feed-Reader, für die sprechenden Permalinks oder einfach nur damit ich meine Artikel über die WordPress Oberfläche schneller wieder finde.</p>



<p>Ich würde mir wünschen, dass Micro.blog einfach immer den Text oder die Summary nutzen würde und den Titel nur als Fallback. Von mir aus auch abhängig vom <a href="https://www.w3.org/TR/post-type-discovery/">Post-Type</a>.</p>



<p>Aktuell gibt es für mich aber nur zwei Möglichkeiten:</p>



<ul>
<li>Ich lasse den Titel weg -&gt; Micro.blog zeigt den vollen Text an und im Feed-Reader siehts scheiße aus</li>
<li>Ich schreibe einen Titel -&gt; Micro.blog zeigt nur den Titel an, aber im Feed-Reader siehts gut aus</li>
</ul>



<p>Es gibt natürlich auch noch andere Lösungen, aber die sind immer mit Arbeit verbunden: HTTP Agent auslesen und nur für Micro.blog den Titel ausblenden, <a href="https://github.com/glueckpress/micro.blog">extra Feed für Micro.blog</a>, …</p>



<p>Am Schluss ist Micro.blog aber nur exemplarisch für eine generelle Entwicklung in der IndieWeb Community.</p>



<p>Peter Molnar hat in einem <a href="https://petermolnar.net/i-want-the-blogs-back/">ähnlichen Zusammenhang</a> etwas sehr passendes dazu geschrieben:</p>



<blockquote>
<p>If I look at my wall, my timeline, or any other stream, it’s a mess  which I’m not proud of. It’s a never-ending scroll of things, without  structure, without separating the less important from the more  important, without me, without focus. <em>“regaining focus” is becoming much of a buzzterm but there is truth behind it.</em></p>
<a href="https://petermolnar.net/i-want-the-blogs-back/index.html">I want the blogs back</a>
</blockquote>



<p><br />Wahrscheinlich sind es nicht die fehlenden Titel die mich aufregen, sondern die Flut an unstrukturierten, zusammenhanglosen Microblogposts, die ich eigentlich gar nicht in meinem Feed-Reader haben will.</p>



<p>…aber das ist eine andere Geschichte.</p>