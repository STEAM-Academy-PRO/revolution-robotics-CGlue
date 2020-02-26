#ifndef COMPONENT_FOO_H_
#define COMPONENT_FOO_H_

#ifndef COMPONENT_TYPES_FOO_H_
#define COMPONENT_TYPES_FOO_H_

#include "some_header.h"
#include <stdint.h>

typedef void (*function_ptr)(uint32_t arg);
typedef uint32_t BarType_t;

#endif /* COMPONENT_TYPES_FOO_H_ */

void foo_Write_port(BarType_t value);

#endif /* COMPONENT_FOO_H_ */
