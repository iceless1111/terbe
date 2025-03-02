# Terbe
A simple Python Package makes you code faster


## Simple show

```python3
import subprocess
status = subprocess.run(["python3", "-m", "rich"])
print("Exit code is:", status)
```

is same to 

```python3
from terbe import coding
status = coding.Sandbox(["path/to/rich"])
print("Exit code is:", status)
```

## Installation

1. Download `terbe- ... .tar.gz`, it might in dist/
2. Install
   ```bash
   pip install terbe- ... .tar.gz
   ```
