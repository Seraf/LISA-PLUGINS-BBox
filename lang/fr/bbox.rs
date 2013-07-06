! array chaines = une deux trois quatre cinq six sept huit neuf dix onze douze suivante précédente precedente

+ met la (@chaines)[*]
- <call>change_channel <star1></call>

+ (augmente|augmenter|monte|monter|baisse|baisser|descend|descendre) le (son|volume) [*]
- <call>change_volume <star1></call>

+ (chaine|chaîne) (@chaines)[*]
- <call>change_channel <star2></call>

+ enregistre (cette) (chaine|chaîne)[*]
- <call>rec_channel <star1></call>

+ enregistre la (@chaines)[*]
- <call>rec_channel <star></call>

+ met sur pause
- <call>pause_channel</call>

+ met sur pause la (@chaines)[*]
- <call>pause_channel <star></call>

> object change_channel python
from BBox.modules.bbox import BBox
return BBox().change_channel(args)
< object

> object change_volume python
from BBox.modules.bbox import BBox
return BBox().change_volume(args)
< object

> object rec_channel python
from BBox.modules.bbox import BBox
return BBox().rec_channel(args)
< object

> object pause_channel python
from BBox.modules.bbox import BBox
if args:
    return BBox().pause_channel(args)
else:
    return BBox().pause_channel()
< object