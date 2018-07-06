## DFPWMX File Format:  

```
\x00         [Opening Byte]
DFPWMX       [Magic Signature]
"B"          [Start of INFO_TAG]
\x01 | \x02  [encoded With | Without MixedStream Format]
             [Where a "|" Stands for OR]
4 Bytes      [If Mixed Stream]
\x00         [End of Data.]
"F"          [Start of File info]
2 Bytes      [Total number of files.]
\x00         [You know what this is now...]
4 Bytes \x00 [Size of individual files. Struct packed.]
\xff         [End of all data]
DFPWM Data...
DFPWM 2 Data...
...
EOF
```

MixedStream Tag [aka MixedStream Format]:  
if **\x02** is present, the file is in **mixedstream mode.**  
the next 4 bytes after the **\x01** is the size of channel packet.  
1024, 2048, 4096, etc...  
channel packet aka X amount of bytes per side.  
