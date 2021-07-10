---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20111117085949/http://petermolnar.eu:80/sysadmin-blog/integer-division-without-divide-functionality/
published: '2011-05-10T07:08:57+00:00'
summary: Division with integers in C, for testing 32 bit max as dividend.
tags:
- C
title: integer division without divide functionality

---

I've found a code in some forum, but it had a bug. Nevertheless, the
function implemented in C:

```c
int DIV ( int dividend , int divisor ) {
  int q = 0;

  while (dividend >= divisor) {
    dividend -= divisor;
    q++;
  }

  return q;
}
```

Although, if time is critical and large numbers are plausible, this will
be SLOW. A more sophisticated one:

```c
tUI32 DIV_tester_UI ( tUI32 dividend, tUI32 divisor )
{
  tUI32 q = 0;
  tUI16 cnt = 0;
  tUI32 tmp = 0;
  tUI32 sft = 1;
  if (divisor != 0 && dividend != 0 && dividend >= divisor )
  {
    if (dividend == divisor)
    {
      q = 1;
    }
    else
    {
      while ( dividend > divisor )
      {
        tmp = dividend;

        while (tmp > divisor)
        {
          tmp = tmp >> 1;
          sft=sft < < 1;
          cnt++;
        }

        if ( tmp != divisor )
        {
          cnt--;
          sft = sft>>1;
        }

        q += sft;
        dividend = dividend - (divisor<<cnt);

        cnt = 0;
        sft = 1;
      }

      if ( dividend == divisor )
      {
        q += 1;
      }

    }
  }

  return q;
}
```