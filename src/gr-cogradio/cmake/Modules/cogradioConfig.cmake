INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_COGRADIO cogradio)

FIND_PATH(
    COGRADIO_INCLUDE_DIRS
    NAMES cogradio/api.h
    HINTS $ENV{COGRADIO_DIR}/include
        ${PC_COGRADIO_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    COGRADIO_LIBRARIES
    NAMES gnuradio-cogradio
    HINTS $ENV{COGRADIO_DIR}/lib
        ${PC_COGRADIO_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(COGRADIO DEFAULT_MSG COGRADIO_LIBRARIES COGRADIO_INCLUDE_DIRS)
MARK_AS_ADVANCED(COGRADIO_LIBRARIES COGRADIO_INCLUDE_DIRS)

