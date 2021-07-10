---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20111116141901/http://petermolnar.eu:80/sysadmin-blog/weighted-average-calculator-code-in-c/
published: '2011-08-23T10:11:04+00:00'
summary: A short code to achieve a very fast weighted filter calculator with
    integers, using few resources.
tags:
- C
title: weighted average calculator code in C

---

This filter was needed for a task that is polled at every 5. millisecond
during the runtime. tUI8, -16, -32 are integer types of 8, 16 and 32
bits.

```c
/* this is for a task that runs at a 5 ms frequency */
tUI8 weighted_filter(int new_sample)
{
    #define FILTER_CONST_WEIGHT                128U    /* total weights */
    #define FILTER_CONST_WEIGHT_SAMPLE        3U    /* weight of new sample */
    #define FILTER_CONST_SHIFT                8U    /* shift by */
    #define FILTER_CONST_SHIFT_VAL            256U    /* shift value */
    #define FILTER_CONST_WEIGHT_SHIFT        7U    /* shift value of weight */

    static tUI32 sample_weighted = 0U;    /* store previous weighted */
    static tBOOL sample_first_run = 1;    /* first run flag */
    tUI8 sample_output = 0;                /* return value */
    tUI32 sample_tmp = 0U;                /* temporary value, needed for calculation */

    /* if first run, set initial values to immediately reach input
     * method would be too slow without this
     */
    if (sample_first_run == 1)
    {
        sample_first_run = 0;        /* no more first runs */
        sample_output = new_sample;    /* return the input value */
        sample_weighted = (tUI32)(new_sample ) << FILTER_CONST_SHIFT;    /* weighted initial value with offset */
    }
    else
    {
        sample_tmp = new_sample;    /* add offset temperature to be in unsigned range */

        sample_tmp = sample_tmp >> FILTER_CONST_WEIGHT_SHIFT; /* divide by total weights */
        sample_tmp = (sample_weighted + (FILTER_CONST_SHIFT_VAL>>1) -1 ) >> FILTER_CONST_SHIFT;    /* round and divide by shift | need to be kept in one row! */
        sample_output = (tUI8)sample_tmp;    /* output value */
    }

return (sample_output);
}
```