---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624125549/https://petermolnar.net/how-to-compile-percona-server-with-xtradb-5-5-for-arm-armhf/
published: '2013-03-02T17:01:01+00:00'
summary: To make Percona run on armhf architecture there are only small changes
    need to be applied.
tags:
- android
title: How to compile Percona Server with XtraDB 5.5 for ARM ( armhf )

---

I had a rough time getting a Percona run in a chrooted, bootstrapped
Debian running beside Android on my previous phone, but it's now done.

Get the latest code from Percona sources[^1], for me, it was
5.5.29-rel29.4 therefore I'll write the docs for this version.

```bash
#!/bin/bash

cd /usr/src
wget http://www.percona.com/redir/downloads/Percona-Server-5.5/Percona-Server-5.5.29-29.4/source/Percona-Server-5.5.29-rel29.4.tar.gz
tar xzf Percona-Server-5.5.29-rel29.4.tar.gz
wget http://pastebin.com/raw.php?i=QXQNDbtc -OPercona-Server-5.5.29-rel29.4.armhf.patch
cd Percona-Server-5.5.29-rel29.4
patch -p0 < ../Percona-Server-5.5.29-rel29.4.armhf.patch
cmake . -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_CONFIG=mysql_release -DFEATURE_SET=community -DWITH_EMBEDDED_SERVER=OFF
```

That's it. The pastebin code is mine, I'll copy it here as well:

```diff
--- sql-common/client_plugin.c  2013-01-07 06:29:49.000000000 +0000
+++ sql-common/client_plugin.c  2013-03-02 11:26:32.180009884 +0000
@@ -233,11 +233,13 @@
 {
   MYSQL mysql;
   struct st_mysql_client_plugin **builtin;
+  va_list unused;

   if (initialized)
     return 0;

   bzero(&mysql, sizeof(mysql)); /* dummy mysql for set_mysql_extended_error */
+  bzero(&unused, sizeof(unused)); /* suppress uninitialized-value warnings */

   pthread_mutex_init(&LOCK_load_client_plugin, MY_MUTEX_INIT_SLOW);
   init_alloc_root(&mem_root, 128, 128);
@@ -249,7 +251,7 @@
   pthread_mutex_lock(&LOCK_load_client_plugin);

   for (builtin= mysql_client_builtins; *builtin; builtin++)
-    add_plugin(&mysql, *builtin, 0, 0, 0);
+    add_plugin(&mysql, *builtin, 0, 0, unused);

   pthread_mutex_unlock(&LOCK_load_client_plugin);

@@ -293,11 +295,15 @@
 mysql_client_register_plugin(MYSQL *mysql,
                              struct st_mysql_client_plugin *plugin)
 {
+  va_list unused;
+
   if (is_not_initialized(mysql, plugin->name))
     return NULL;

   pthread_mutex_lock(&LOCK_load_client_plugin);

+  bzero(&unused, sizeof(unused)); /* suppress uninitialized-value warnings */
+
   /* make sure the plugin wasn't loaded meanwhile */
   if (find_plugin(plugin->name, plugin->type))
   {
@@ -307,7 +313,7 @@
     plugin= NULL;
   }
   else
-    plugin= add_plugin(mysql, plugin, 0, 0, 0);
+    plugin= add_plugin(mysql, plugin, 0, 0, unused);

   pthread_mutex_unlock(&LOCK_load_client_plugin);
   return plugin;
--- sql/query_response_time.cc  2013-01-07 06:29:49.000000000 +0000
+++ sql/query_response_time.cc  2013-03-02 12:41:16.290010827 +0000
@@ -198,7 +198,7 @@
   /* The lock for atomic operations on m_count and m_total.  Only actually
   used on architectures that do not have atomic implementation of atomic
   operations. */
-  my_atomic_rwlock_t time_collector_lock;
+  mutable my_atomic_rwlock_t time_collector_lock;
   uint32   m_count[OVERALL_POWER_COUNT + 1];
   uint64   m_total[OVERALL_POWER_COUNT + 1];
 };
```

[^1]: <http://www.percona.com/downloads/Percona-Server-5.5/LATEST/source/>