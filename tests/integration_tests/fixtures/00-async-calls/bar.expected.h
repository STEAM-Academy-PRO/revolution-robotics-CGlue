#ifndef COMPONENT_BAR_H_
#define COMPONENT_BAR_H_

#ifndef COMPONENT_TYPES_BAR_H_
#define COMPONENT_TYPES_BAR_H_

#include <stdint.h>

typedef uint32_t BarType_t;

typedef enum {
    AsyncCommand_None,
    AsyncCommand_Start,
    AsyncCommand_Continue,
    AsyncCommand_Cancel
} AsyncCommand_t;

typedef enum {
    AsyncResult_Pending,
    AsyncResult_Ok
} AsyncResult_t;

#endif /* COMPONENT_TYPES_BAR_H_ */

void bar_Run_no_args(void);
void bar_Run_with_args(uint32_t arg, BarType_t* result);
AsyncResult_t bar_AsyncRunnable_async_runnable(AsyncCommand_t asyncCommand);

#endif /* COMPONENT_BAR_H_ */
