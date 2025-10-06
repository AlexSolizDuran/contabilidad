from .empresa import (EmpresaCreateSerializer,
                      EmpresaDetailSerializer,
                      EmpresaListSerializer)
from .rol import (RolEmpresaCreateSerializer,
                  RolEmpresaListSerializer,
                  RolEmpresaDetailSerializer)
from .user_empresa import (UserEmpresaCreateSerializer,
                           UserEmpresaListSerializer,
                           UserEmpresaDetailSerializer,CustomSerializer)
from .permiso import PermisoSerializer,PermisoDetailSerializer
from .login_empresa import LoginEmpresaSerializer
from .custom import (CustomCreateSerializer,
                     CustomDetailSerializer,
                     CustomListSerializer)