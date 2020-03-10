#include "runtime.h"
#include "utils.h"

static foo_Instance_t foo_instance_foo1;
static foo_Instance_t foo_instance_foo2;
static bar_Instance_t bar_instance_bar1;
static bar_Instance_t bar_instance_bar2;

/* bar1_no_args_async_call */
static AsyncOperationState_t bar1_no_args_async_call_state = AsyncState_Idle;
static AsyncCommand_t bar1_no_args_async_call_command = AsyncCommand_None;
static bar_Instance_t bar1_no_args_async_call_argument_instance;
static void bar1_no_args_async_call_Update(void);

/* bar1_with_args_async_call */
static AsyncOperationState_t bar1_with_args_async_call_state = AsyncState_Idle;
static AsyncCommand_t bar1_with_args_async_call_command = AsyncCommand_None;
static bar_Instance_t bar1_with_args_async_call_argument_instance;
static uint32_t bar1_with_args_async_call_argument_arg;
static BarType_t bar1_with_args_async_call_argument_result;
static void bar1_with_args_async_call_Update(void);

/* bar2_no_args_async_call */
static AsyncOperationState_t bar2_no_args_async_call_state = AsyncState_Idle;
static AsyncCommand_t bar2_no_args_async_call_command = AsyncCommand_None;
static bar_Instance_t bar2_no_args_async_call_argument_instance;
static void bar2_no_args_async_call_Update(void);

/* bar2_with_args_async_call */
static AsyncOperationState_t bar2_with_args_async_call_state = AsyncState_Idle;
static AsyncCommand_t bar2_with_args_async_call_command = AsyncCommand_None;
static bar_Instance_t bar2_with_args_async_call_argument_instance;
static uint32_t bar2_with_args_async_call_argument_arg;
static BarType_t bar2_with_args_async_call_argument_result;
static void bar2_with_args_async_call_Update(void);

void bar1_no_args_async_call_Update(void)
{
    __disable_irq();
    AsyncCommand_t command = bar1_no_args_async_call_command;
    bar1_no_args_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar1_no_args_async_call_state = AsyncState_Busy;
            __enable_irq();

            bar_Run_no_args(
                &bar1_no_args_async_call_argument_instance);

            bar1_no_args_async_call_state = AsyncState_Done;
            break;

        case AsyncCommand_Cancel:
            __enable_irq();
            bar1_no_args_async_call_state = AsyncState_Idle;
            break;

        default:
            __enable_irq();
            break;
    }
}

void bar1_with_args_async_call_Update(void)
{
    __disable_irq();
    AsyncCommand_t command = bar1_with_args_async_call_command;
    bar1_with_args_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar1_with_args_async_call_state = AsyncState_Busy;
            __enable_irq();

            bar_Run_with_args(
                &bar1_with_args_async_call_argument_instance,
                bar1_with_args_async_call_argument_arg,
                &bar1_with_args_async_call_argument_result);

            bar1_with_args_async_call_state = AsyncState_Done;
            break;

        case AsyncCommand_Cancel:
            __enable_irq();
            bar1_with_args_async_call_state = AsyncState_Idle;
            break;

        default:
            __enable_irq();
            break;
    }
}

void bar2_no_args_async_call_Update(void)
{
    __disable_irq();
    AsyncCommand_t command = bar2_no_args_async_call_command;
    bar2_no_args_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar2_no_args_async_call_state = AsyncState_Busy;
            __enable_irq();

            bar_Run_no_args(
                &bar2_no_args_async_call_argument_instance);

            bar2_no_args_async_call_state = AsyncState_Done;
            break;

        case AsyncCommand_Cancel:
            __enable_irq();
            bar2_no_args_async_call_state = AsyncState_Idle;
            break;

        default:
            __enable_irq();
            break;
    }
}

void bar2_with_args_async_call_Update(void)
{
    __disable_irq();
    AsyncCommand_t command = bar2_with_args_async_call_command;
    bar2_with_args_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar2_with_args_async_call_state = AsyncState_Busy;
            __enable_irq();

            bar_Run_with_args(
                &bar2_with_args_async_call_argument_instance,
                bar2_with_args_async_call_argument_arg,
                &bar2_with_args_async_call_argument_result);

            bar2_with_args_async_call_state = AsyncState_Done;
            break;

        case AsyncCommand_Cancel:
            __enable_irq();
            bar2_with_args_async_call_state = AsyncState_Idle;
            break;

        default:
            __enable_irq();
            break;
    }
}

void Runtime_RaiseEvent_loop(void)
{
    bar1_no_args_async_call_Update();
    bar1_with_args_async_call_Update();
    bar2_no_args_async_call_Update();
    bar2_with_args_async_call_Update();
}

AsyncOperationState_t foo_Async_no_args_Call(foo_Instance_t* instance)
{
    if (instance == &foo_instance_foo1)
    {
        AsyncOperationState_t returned_state = AsyncState_Busy;
        bar1_no_args_async_call_command = AsyncCommand_None;
        __disable_irq();
        if (bar1_no_args_async_call_state == AsyncState_Idle || bar1_no_args_async_call_state == AsyncState_Done)
        {
            bar1_no_args_async_call_state = AsyncState_Started;
            __enable_irq();


            returned_state = AsyncState_Started;
            bar1_no_args_async_call_command = AsyncCommand_Start;
        }
        else
        {
            __enable_irq();
        }
        return returned_state;
    }
    if (instance == &foo_instance_foo2)
    {
        AsyncOperationState_t returned_state = AsyncState_Busy;
        bar2_no_args_async_call_command = AsyncCommand_None;
        __disable_irq();
        if (bar2_no_args_async_call_state == AsyncState_Idle || bar2_no_args_async_call_state == AsyncState_Done)
        {
            bar2_no_args_async_call_state = AsyncState_Started;
            __enable_irq();


            returned_state = AsyncState_Started;
            bar2_no_args_async_call_command = AsyncCommand_Start;
        }
        else
        {
            __enable_irq();
        }
        return returned_state;
    }
    return AsyncState_Busy;
}

AsyncOperationState_t foo_Async_no_args_GetResult(foo_Instance_t* instance)
{
    if (instance == &foo_instance_foo1)
    {
        AsyncOperationState_t returned_state;
        __disable_irq();
        switch (bar1_no_args_async_call_state)
        {
            case AsyncState_Done:
                bar1_no_args_async_call_state = AsyncState_Idle;
                __enable_irq();
                returned_state = AsyncState_Done;
                break;

            case AsyncState_Started:
                __enable_irq();
                returned_state = AsyncState_Busy;
                break;

            default:
                __enable_irq();
                returned_state = bar1_no_args_async_call_state;
                break;
        }
        return returned_state;
    }
    if (instance == &foo_instance_foo2)
    {
        AsyncOperationState_t returned_state;
        __disable_irq();
        switch (bar2_no_args_async_call_state)
        {
            case AsyncState_Done:
                bar2_no_args_async_call_state = AsyncState_Idle;
                __enable_irq();
                returned_state = AsyncState_Done;
                break;

            case AsyncState_Started:
                __enable_irq();
                returned_state = AsyncState_Busy;
                break;

            default:
                __enable_irq();
                returned_state = bar2_no_args_async_call_state;
                break;
        }
        return returned_state;
    }
    return AsyncState_Busy;
}

void foo_Async_no_args_Cancel(foo_Instance_t* instance)
{
    if (instance == &foo_instance_foo1)
    {
        bar1_no_args_async_call_command = AsyncCommand_Cancel;
    }
    if (instance == &foo_instance_foo2)
    {
        bar2_no_args_async_call_command = AsyncCommand_Cancel;
    }
}

AsyncOperationState_t foo_Async_with_args_Call(foo_Instance_t* instance, uint32_t arg)
{
    if (instance == &foo_instance_foo1)
    {
        AsyncOperationState_t returned_state = AsyncState_Busy;
        bar1_with_args_async_call_command = AsyncCommand_None;
        __disable_irq();
        if (bar1_with_args_async_call_state == AsyncState_Idle || bar1_with_args_async_call_state == AsyncState_Done)
        {
            bar1_with_args_async_call_state = AsyncState_Started;
            __enable_irq();

            bar1_with_args_async_call_argument_arg = arg;

            returned_state = AsyncState_Started;
            bar1_with_args_async_call_command = AsyncCommand_Start;
        }
        else
        {
            __enable_irq();
        }
        return returned_state;
    }
    if (instance == &foo_instance_foo2)
    {
        AsyncOperationState_t returned_state = AsyncState_Busy;
        bar2_with_args_async_call_command = AsyncCommand_None;
        __disable_irq();
        if (bar2_with_args_async_call_state == AsyncState_Idle || bar2_with_args_async_call_state == AsyncState_Done)
        {
            bar2_with_args_async_call_state = AsyncState_Started;
            __enable_irq();

            bar2_with_args_async_call_argument_arg = arg;

            returned_state = AsyncState_Started;
            bar2_with_args_async_call_command = AsyncCommand_Start;
        }
        else
        {
            __enable_irq();
        }
        return returned_state;
    }
    return AsyncState_Busy;
}

AsyncOperationState_t foo_Async_with_args_GetResult(foo_Instance_t* instance, BarType_t* result)
{
    if (instance == &foo_instance_foo1)
    {
        AsyncOperationState_t returned_state;
        __disable_irq();
        switch (bar1_with_args_async_call_state)
        {
            case AsyncState_Done:
                if (result)
                {
                    *result = bar1_with_args_async_call_argument_result;
                }
                bar1_with_args_async_call_state = AsyncState_Idle;
                __enable_irq();
                returned_state = AsyncState_Done;
                break;

            case AsyncState_Started:
                __enable_irq();
                returned_state = AsyncState_Busy;
                break;

            default:
                __enable_irq();
                returned_state = bar1_with_args_async_call_state;
                break;
        }
        return returned_state;
    }
    if (instance == &foo_instance_foo2)
    {
        AsyncOperationState_t returned_state;
        __disable_irq();
        switch (bar2_with_args_async_call_state)
        {
            case AsyncState_Done:
                if (result)
                {
                    *result = bar2_with_args_async_call_argument_result;
                }
                bar2_with_args_async_call_state = AsyncState_Idle;
                __enable_irq();
                returned_state = AsyncState_Done;
                break;

            case AsyncState_Started:
                __enable_irq();
                returned_state = AsyncState_Busy;
                break;

            default:
                __enable_irq();
                returned_state = bar2_with_args_async_call_state;
                break;
        }
        return returned_state;
    }
    return AsyncState_Busy;
}

void foo_Async_with_args_Cancel(foo_Instance_t* instance)
{
    if (instance == &foo_instance_foo1)
    {
        bar1_with_args_async_call_command = AsyncCommand_Cancel;
    }
    if (instance == &foo_instance_foo2)
    {
        bar2_with_args_async_call_command = AsyncCommand_Cancel;
    }
}
