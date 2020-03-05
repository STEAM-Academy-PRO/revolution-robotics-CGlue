#ifndef GENERATED_RUNTIME_H_
#define GENERATED_RUNTIME_H_

#include "some_header.h"
#include <stdint.h>
#include <stdio.h>

typedef uint32_t BarType_t;

typedef struct {
    uint8_t* bytes;
    size_t count;
} ByteArray_t;
typedef void (*function_ptr)(BarType_t arg, ByteArray_t* data);

#define COMPONENT_TYPES_FOO_H_
#define COMPONENT_TYPES_BAR_H_

#include "components/foo/foo.h"
#include "components/bar/bar.h"


#endif /* GENERATED_RUNTIME_H */
