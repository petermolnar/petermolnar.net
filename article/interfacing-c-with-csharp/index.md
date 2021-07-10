---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624125641/https://petermolnar.net/interfacing-c-with-csharp/
published: '2012-05-08T07:30:51+00:00'
summary: How to send and receive a string between C# and C.
tags:
- C
title: String interchange between C# to and ANSI C DLL

---

Recently we had some problems interfacing a C\# code with a C (
especially MinGW ) DLL. The main problem was that we needed to
interchange strings, send ans received from both directions.

## Sending a registry entry from C\# to C

### C

```cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;
using System.Threading;

namespace CODE
{
    public unsafe class Connector
    {
        private string PathKey = "Path";
        // needs to be constant...
        private const string PathToCDLL = @"C:pathtocdll";

        public void InitPath()
        {
            string Path = new Globals().getRegistryEntry(this.PathKey);
            // string characters are 2 bytes long in C#, C needs 1 byte chars:
            System.Text.ASCIIEncoding encoding = new System.Text.ASCIIEncoding();
            Byte[] path = encoding.GetBytes( Path );
            init_path_c(path);
        }

        [DllImport(PathToCDLL, EntryPoint = "init_path", ExactSpelling = true, CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl)]
        private static extern void init_path_c([MarshalAs(UnmanagedType.LPArray)] byte[] Path );
    }
}
```

### C

```c
char* global_path;
void init_path( char* path )
{
      global_path = path;
}
```

## Receiving a string in C\# from C

### CS

```cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;
using System.Threading;

namespace CODE
{
    public unsafe class Connector
    {
        public string getCString()
        {
            IntPtr strPtr = Marshal.AllocHGlobal(Marshal.SizeOf(typeof(int)));
            get_c_string(strPtr);
            return Marshal.PtrToStringAnsi(strPtr);
        }

        [DllImport(PathToCDLL, EntryPoint = "c_string", ExactSpelling = true, CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl)]
        private static extern void get_c_string( IntPtr Path );

    }
}
```

### C

```c
#include <string.h>

void c_string( char* path )
{  
  char* str = "This is a test string";
  strcpy ( path, str );
}
```