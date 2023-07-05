# PreImage
PreImage is a util for making lightweight python deployments simple by automatically optimizing dependency trees. 

### TODO: 
- support for local imports (e.g. from . import file)
- Test aliased imports (e.g. import numpy as np)
- Support for import * (e.g. from numpy import *)
- Recursive import scanning from local imports (e.g. import <local_module> also should scan <local_module> for imports and list them)
- (Later) Import cleanup. E.g. if a package is imported but not used, it should be removed from the import list. Additionally, if a package is imported but only a subset of its functions are used, it should be changed to only import those functions. (e.g. from numpy import array, zeros, ones)
- (Later) Auto requirements.txt + dockerfile generation. If a package is imported, it should be added to the dockerfile.
