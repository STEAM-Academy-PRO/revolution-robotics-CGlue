#ifndef COMPONENT_FOO_H_
#define COMPONENT_FOO_H_

#ifndef COMPONENT_TYPES_FOO_H_
#define COMPONENT_TYPES_FOO_H_

#include "some_header.h"
#include <stdint.h>

typedef uint32_t BarType_t;
typedef void (*function_ptr)(BarType_t arg);

#endif /* COMPONENT_TYPES_FOO_H_ */

void foo_Run_runnable_name(BarType_t arg);

#endif /* COMPONENT_FOO_H_ */
