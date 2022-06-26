# FastRecord

Lightweight library for storing a sequence of binary records, which supports writer and reader for DL training samples.


## File Format

**Storage Layout:**
```
+-----------------------------------+---------------------------------------+
|         checksum                  |             N                         |
+-----------------------------------+---------------------------------------+
|         checksums                 |           offsets                     |
+---------------------+---------------------+--------+----------------------+
|      sample 1       |      sample 2       | ....   |      sample N        |
+---------------------+---------------------+--------+----------------------+
```

**Fields:**

| field     | size (bytes)                  | description                     |
|-----------|-------------------------------|---------------------------------|
| checksum  | 4                             | CRC32 checksum of all data      |
| N         | 8                             | number of samples               |
| checksums | 4 * N                         | CRC32 checksum of each sample   |
| offsets   | 8 * N                         | byte offset of each sample      |
| sample i  | offsets[i + 1] - offsets[i]   | data of the i-th sample         |

## Get Started

### Requirements

- OS: Linux
- Python >= 3.6
- Pytorch >= 1.6
- [libaio 0.8.3](https://pypi.org/project/libaio/)

```
