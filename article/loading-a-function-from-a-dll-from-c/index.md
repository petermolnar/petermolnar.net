---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120413193512/http://petermolnar.eu:80/linux-tech-coding/loading-a-function-from-a-dll-from-c/
published: '2012-01-23T09:01:18+00:00'
summary: Calling functions from a DLL in a C code? Don't. But it's possible.
tags:
- C
title: Loading a function from a DLL from C

---

I was doing one of the nastiest task ever in the last few weeks: call a
function from a DLL written in C++ from native C code. Here's how to do
it with latest MinGW.

The DLL contains a function, named `Test`, returning an `int`, and have
one single `int` parameter and - how suprising - returns an `int` as
status.

`dllhandler.h`

```c
#ifndef DLLHANDLER_C_
#define DLLHANDLER_C_

#include <windows.h>
#include <winbase.h>
#include <windef.h>
#include <stdio.h>

typedef int (*TestFunc)(int);

int loadDLL( void );

#endif
```

`dllhandler.c`

```c
#include "dllhandler.h"

int loadDLL( )
{
    int status = 0;
    TestFunc _TestFunc;
    HINSTANCE testLibrary = LoadLibrary("test.dll");

    if (testLibrary)
    {
        _TestFunc = (TestFunc)GetProcAddress(testLibrary, "Test");
        if (_TestFunc)
        {
            status = _TestFunc();
        }
        FreeLibrary(serialLibrary);
    }
    return status;
}
```