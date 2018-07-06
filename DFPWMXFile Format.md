## DFPWMX File Format:  

```
\x00        [Opening Byte]
DFPWMX      [Magic Signature]
B           [Start of INFO_TAG]
\x01 | \x02 [encoded With | Without MixedStream Format]

Where a "|" Stands for OR
```

MixedStream Tag [aka MixedStream Format]:  
if **\x02** is present, the file is in **mixedstream mode.**  
the next 4 bytes after the **\x01** is the size of channel packet.  
1024, 2048, 4096, etc...  
channel packet aka X amount of bytes per side.