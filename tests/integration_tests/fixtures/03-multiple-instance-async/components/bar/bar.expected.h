#ifndef COMPONENT_BAR_H_
#define COMPONENT_BAR_H_

#ifndef COMPONENT_TYPES_BAR_H_
#define COMPONENT_TYPES_BAR_H_

#include <stdint.h>

typedef uint32_t BarType_t;

typedef struct {
} bar_Instance_t;

#endif /* COMPONENT_TYPES_BAR_H_ */

/* Begin User Code Section: Declarations */

/* End User Code Section: Declarations */

void bar_Run_no_args(bar_Instance_t* instance);
void bar_Run_with_args(bar_Instance_t* instance, uint32_t arg, BarType_t* result);

#endif /* COMPONENT_BAR_H_ */
