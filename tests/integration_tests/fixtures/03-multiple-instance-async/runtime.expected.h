#ifndef GENERATED_RUNTIME_H_
#define GENERATED_RUNTIME_H_

#include <stdint.h>


typedef struct {
} bar_Instance_t;

typedef enum {
    AsyncOperationState_Idle,
    AsyncOperationState_Started,
    AsyncOperationState_Busy,
    AsyncOperationState_Done
} AsyncOperationState_t;

typedef enum {
    AsyncCommand_None,
    AsyncCommand_Start,
    AsyncCommand_Continue,
    AsyncCommand_Cancel
} AsyncCommand_t;
typedef uint32_t BarType_t;

typedef struct {
} foo_Instance_t;

#define COMPONENT_TYPES_FOO_H_
#define COMPONENT_TYPES_BAR_H_

#include "components/foo/foo.h"
#include "components/bar/bar.h"

void Runtime_RaiseEvent_loop(void);

#endif /* GENERATED_RUNTIME_H */
