# Horary Workflows

Horary astrology is divination from a horoscope. In *Horary Examples: Traditional Horary Astrology*, Kathryn Silvestre writes: "Someone asks a question on a matter of importance to them. When the question reaches the ears or eyes of an astrologer with the knowledge to judge the chart, the question is born." However, you may take a different approach:

- **Time:** If the question is asked in writing, do you use
    * the moment it landed in your inbox?
    * the moment you opened it?
- **Location**: If the question is asked over a distance (most likely), do you use
    * *your* coordinates?
    * the coordinates of the querent? (an extra thing to ask for/look up)
    * the midpoint/average between the two? (arithmetic...)

Assuming you use the more conventional approach, `now` should be sufficient for most horary questions, and I suggest saving the chart you cast with the `--save` flag. A chart run with `now --save` will have a default title of the UTC date and time, like `2025-09-17 19:52: 12 UTC`, which you may want to replace with the question asked. We'll talk about how to modify saved charts under [Advanced Usage](./60-advanced-usage.md).

If you have location preferences, you can use `cast` instead. You lose the seconds-accuracy of `ephem now`, but replace it with geographic precision.
