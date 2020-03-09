#include "runtime.h"
#include "utils.h"


/* bar_no_args_async_call */
static AsyncOperationState_t bar_no_args_async_call_state = AsyncState_Idle;
static AsyncCommand_t bar_no_args_async_call_command = AsyncCommand_None;
static void bar_no_args_async_call_Update(void);

/* bar_with_args_async_call */
static AsyncOperationState_t bar_with_args_async_call_state = AsyncState_Idle;
static AsyncCommand_t bar_with_args_async_call_command = AsyncCommand_None;
static uint32_t bar_with_args_async_call_argument_arg;
static BarType_t bar_with_args_async_call_argument_result;
static void bar_with_args_async_call_Update(void);

void bar_no_args_async_call_Update(void)
{
    __disable_irq();
    AsyncCommand_t command = bar_no_args_async_call_command;
    bar_no_args_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar_no_args_async_call_state = AsyncState_Busy;
            __enable_irq();

            bar_Run_no_args();

            bar_no_args_async_call_state = AsyncState_Done;
            break;

        case AsyncCommand_Cancel:
            __enable_irq();
            bar_no_args_async_call_state = AsyncState_Idle;
            break;

        default:
            __enable_irq();
            break;
    }
}

void bar_with_args_async_call_Update(void)
{
    __disable_irq();
    AsyncCommand_t command = bar_with_args_async_call_command;
    bar_with_args_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar_with_args_async_call_state = AsyncState_Busy;
            __enable_irq();

            bar_Run_with_args(
                bar_with_args_async_call_argument_arg,
                &bar_with_args_async_call_argument_result);

            bar_with_args_async_call_state = AsyncState_Done;
            break;

        case AsyncCommand_Cancel:
            __enable_irq();
            bar_with_args_async_call_state = AsyncState_Idle;
            break;

        default:
            __enable_irq();
            break;
    }
}

void Runtime_RaiseEvent_loop(void)
{
    bar_no_args_async_call_Update();
    bar_with_args_async_call_Update();
}

AsyncOperationState_t foo_Async_no_args_Call(void)
{
    AsyncOperationState_t returned_state = AsyncState_Busy;
    bar_no_args_async_call_command = AsyncCommand_None;
    __disable_irq();
    if (bar_no_args_async_call_state == AsyncState_Idle || bar_no_args_async_call_state == AsyncState_Done)
    {
        bar_no_args_async_call_state = AsyncState_Started;
        __enable_irq();


        returned_state = AsyncState_Started;
        bar_no_args_async_call_command = AsyncCommand_Start;
    }
    else
    {
        __enable_irq();
    }
    return returned_state;
}

AsyncOperationState_t foo_Async_no_args_GetResult(void)
{
    AsyncOperationState_t returned_state;
    __disable_irq();
    switch (bar_no_args_async_call_state)
    {
        case AsyncState_Done:
            bar_no_args_async_call_state = AsyncState_Idle;
            __enable_irq();
            returned_state = AsyncState_Done;
            break;

        case AsyncState_Started:
            __enable_irq();
            returned_state = AsyncState_Busy;
            break;

        default:
            __enable_irq();
            returned_state = bar_no_args_async_call_state;
            break;
    }
    return returned_state;
}

void foo_Async_no_args_Cancel(void)
{
    bar_no_args_async_call_command = AsyncCommand_Cancel;
}

AsyncOperationState_t foo_Async_with_args_Call(uint32_t arg)
{
    AsyncOperationState_t returned_state = AsyncState_Busy;
    bar_with_args_async_call_command = AsyncCommand_None;
    __disable_irq();
    if (bar_with_args_async_call_state == AsyncState_Idle || bar_with_args_async_call_state == AsyncState_Done)
    {
        bar_with_args_async_call_state = AsyncState_Started;
        __enable_irq();

        bar_with_args_async_call_argument_arg = arg;

        returned_state = AsyncState_Started;
        bar_with_args_async_call_command = AsyncCommand_Start;
    }
    else
    {
        __enable_irq();
    }
    return returned_state;
}

AsyncOperationState_t foo_Async_with_args_GetResult(BarType_t* result)
{
    AsyncOperationState_t returned_state;
    __disable_irq();
    switch (bar_with_args_async_call_state)
    {
        case AsyncState_Done:
            if (result)
            {
                *result = bar_with_args_async_call_argument_result;
            }
            bar_with_args_async_call_state = AsyncState_Idle;
            __enable_irq();
            returned_state = AsyncState_Done;
            break;

        case AsyncState_Started:
            __enable_irq();
            returned_state = AsyncState_Busy;
            break;

        default:
            __enable_irq();
            returned_state = bar_with_args_async_call_state;
            break;
    }
    return returned_state;
}

void foo_Async_with_args_Cancel(void)
{
    bar_with_args_async_call_command = AsyncCommand_Cancel;
}
