#ifndef GENERATED_RUNTIME_H_
#define GENERATED_RUNTIME_H_

#include <stdint.h>


typedef struct {
    uint32_t var1;
} foo_Instance_t;
typedef void (*FuncPtr_t)(foo_Instance_t* instance);

typedef enum {
    QueueStatus_Empty,
    QueueStatus_Ok,
    QueueStatus_Overflow
} QueueStatus_t;

#define COMPONENT_TYPES_FOO_H_

#include "components/foo/foo.h"

void Runtime_RaiseEvent_OnInit(void);

#endif /* GENERATED_RUNTIME_H */
