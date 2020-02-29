#ifndef COMPONENT_FOO_H_
#define COMPONENT_FOO_H_

#ifndef COMPONENT_TYPES_FOO_H_
#define COMPONENT_TYPES_FOO_H_

#include <stdint.h>

typedef struct {
    uint32_t var1;
} foo_Instance_t;

#endif /* COMPONENT_TYPES_FOO_H_ */

void foo_Run_Runnable(foo_Instance_t* instance);

#endif /* COMPONENT_FOO_H_ */
