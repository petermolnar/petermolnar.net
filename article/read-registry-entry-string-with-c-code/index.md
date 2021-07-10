---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120413174343/http://petermolnar.eu:80/linux-tech-coding/read-registry-entry-string-with-c-code/
published: '2012-02-07T14:41:42+00:00'
summary: Reading a non-fixed-length string from registry with the help of
    C? Here's how.
tags:
- C
title: Read registry entry string with C code

---

After DLL calling from C[^1] the next nice thing was to read out a
string from the registry.

To be honest I'm now sure we need all the headers included, but
unfortunately I don't have time to test them all. The main point is that
we need to dinamically adjust the size of the buffer to read out the
exact length we need. The returned value behaves the same as it were a
string.

```c
#include <windows.h>
#include <winbase.h>
#include <windef.h>
#include <stdio.h>
#include <string.h>

PPERF_DATA_BLOCK readStringFromRegistry( void* keyname, void* valuename  ) {
  HKEY hkeyPtr;
  DWORD keystatus;
  DWORD buffersize = 1;
  DWORD cbData = buffersize;
  PPERF_DATA_BLOCK PerfData = (PPERF_DATA_BLOCK) malloc( buffersize );

  keystatus = RegOpenKeyEx(HKEY_LOCAL_MACHINE,TEXT(keyname), 0,KEY_READ, &hkeyPtr);
  if (ERROR_SUCCESS == keystatus)
  {
    keystatus = RegQueryValueEx( hkeyPtr, TEXT(valuename),NULL,NULL,(LPBYTE) PerfData,&cbData );

    while( keystatus == ERROR_MORE_DATA )
    {
      buffersize += 1;
      PerfData = (PPERF_DATA_BLOCK) realloc( PerfData, buffersize );
      cbData = buffersize;
      keystatus = RegQueryValueEx( hkeyPtr,TEXT(keyname),NULL,NULL,(LPBYTE) PerfData,&cbData );
    }

  }
  RegCloseKey(hkeyPtr);
  return PerfData;
}
```

[^1]: <https://petermolnar.net/loading-a-function-from-a-dll-from-c/>