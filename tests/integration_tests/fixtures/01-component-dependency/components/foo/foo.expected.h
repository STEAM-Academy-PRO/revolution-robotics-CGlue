#ifndef COMPONENT_FOO_H_
#define COMPONENT_FOO_H_

#ifndef COMPONENT_TYPES_FOO_H_
#define COMPONENT_TYPES_FOO_H_

#include "some_header.h"
#include <stdint.h>
#include <stdio.h>

typedef uint32_t BarType_t;

typedef struct {
    uint8_t* bytes;
    size_t count;
} ByteArray_t;
typedef void (*function_ptr)(BarType_t arg, ByteArray_t* data);

#endif /* COMPONENT_TYPES_FOO_H_ */

/* Begin User Code Section: Declarations */

/* End User Code Section: Declarations */

void foo_Write_port(BarType_t value);

#endif /* COMPONENT_FOO_H_ */
