#ifndef COMPONENT_FOO_H_
#define COMPONENT_FOO_H_

#ifndef COMPONENT_TYPES_FOO_H_
#define COMPONENT_TYPES_FOO_H_

#include <stdint.h>

typedef uint32_t BarType_t;

typedef enum {
    AsyncState_Idle,
    AsyncState_Started,
    AsyncState_Busy,
    AsyncState_Done
} AsyncOperationState_t;

#endif /* COMPONENT_TYPES_FOO_H_ */

AsyncOperationState_t foo_Async_no_args_Call(void);
AsyncOperationState_t foo_Async_no_args_GetResult(void);
void foo_Async_no_args_Cancel(void);
AsyncOperationState_t foo_Async_no_args_async_Call(void);
AsyncOperationState_t foo_Async_no_args_async_GetResult(void);
void foo_Async_no_args_async_Cancel(void);
AsyncOperationState_t foo_Async_with_args_Call(uint32_t arg);
AsyncOperationState_t foo_Async_with_args_GetResult(BarType_t* result);
void foo_Async_with_args_Cancel(void);

#endif /* COMPONENT_FOO_H_ */
