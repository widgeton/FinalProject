from typing import Annotated

from pydantic import Field

Email = Annotated[str, Field(pattern=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$',
                             examples=["user@gmail.com"])]
Pass = Annotated[str, Field(min_length=6, examples=["NjuyT56Yu/U%g"])]
Str = Annotated[str, Field(pattern=r'^[A-Z][a-z]*(\s[A-Z][a-z]*)*$')]
