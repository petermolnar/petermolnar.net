---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624130449/https://petermolnar.net/wordpress-innodb-screams-for-foreign-keys/
published: '2014-07-25T12:02:12+00:00'
summary: No more orphaned data in WordPress if you add FOREIGN keys to your
    InnoDB database.
tags:
- WordPress
title: WordPress + InnoDB screams for FOREIGN keys

---

I've used database cleanup plugins to find orphaned post meta, comment
meta, comment, etc. on a WordPress database in the past.

In case you're using InnoDB[^1] as your MySQL Engine[^2], which is the
default from version 5.5, you might want FOREIGN KEYS to prevent this
kind of orphanage.

Please do not believe the sounds out there that this degrades
performance since it's only in effect when you delete, and with
deletion, you do want a clean delete. It does not effect view/read
performance at all.

```sql
--
-- Constraints for table `wp_commentmeta`
--
ALTER TABLE `wp_commentmeta`
ADD CONSTRAINT `comment_id` FOREIGN KEY (`comment_id`) REFERENCES `wp_comments` (`comment_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `wp_comments`
--
ALTER TABLE `wp_comments`
ADD CONSTRAINT `commet_post_id` FOREIGN KEY (`comment_post_ID`) REFERENCES `wp_posts` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `wp_postmeta`
--
ALTER TABLE `wp_postmeta`
ADD CONSTRAINT `post_id` FOREIGN KEY (`post_id`) REFERENCES `wp_posts` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `wp_posts`
--
ALTER TABLE `wp_posts`
ADD CONSTRAINT `author_id` FOREIGN KEY (`post_author`) REFERENCES `wp_users` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `wp_term_relationships`
--
ALTER TABLE `wp_term_relationships`
ADD CONSTRAINT `term_taxonomy_id` FOREIGN KEY (`term_taxonomy_id`) REFERENCES `wp_term_taxonomy` (`term_taxonomy_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `wp_term_taxonomy`
--
ALTER TABLE `wp_term_taxonomy`
ADD CONSTRAINT `term_id` FOREIGN KEY (`term_id`) REFERENCES `wp_terms` (`term_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `wp_usermeta`
--
ALTER TABLE `wp_usermeta`
ADD CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `wp_users` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;
```

[^1]: <https://dev.mysql.com/doc/refman/5.6/en/innodb-storage-engine.html>

[^2]: <https://dev.mysql.com/doc/refman/5.6/en/storage-engines.html>