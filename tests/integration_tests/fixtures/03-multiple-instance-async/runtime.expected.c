#include "runtime.h"
#include "utils.h"

static foo_Instance_t foo_instance_foo1;
static foo_Instance_t foo_instance_foo2;
static bar_Instance_t bar_instance_bar1;
static bar_Instance_t bar_instance_bar2;
/* Begin User Code Section: Declarations */

/* End User Code Section: Declarations */

/* bar1_no_args_async_call */
static AsyncOperationState_t bar1_no_args_async_call_state = AsyncOperationState_Idle;
static AsyncCommand_t bar1_no_args_async_call_command = AsyncCommand_None;
static void bar1_no_args_async_call_Update(void);

/* bar1_with_args_async_call */
static AsyncOperationState_t bar1_with_args_async_call_state = AsyncOperationState_Idle;
static AsyncCommand_t bar1_with_args_async_call_command = AsyncCommand_None;
static uint32_t bar1_with_args_async_call_argument_arg;
static BarType_t bar1_with_args_async_call_argument_result;
static void bar1_with_args_async_call_Update(void);

/* bar2_no_args_async_call */
static AsyncOperationState_t bar2_no_args_async_call_state = AsyncOperationState_Idle;
static AsyncCommand_t bar2_no_args_async_call_command = AsyncCommand_None;
static void bar2_no_args_async_call_Update(void);

/* bar2_with_args_async_call */
static AsyncOperationState_t bar2_with_args_async_call_state = AsyncOperationState_Idle;
static AsyncCommand_t bar2_with_args_async_call_command = AsyncCommand_None;
static uint32_t bar2_with_args_async_call_argument_arg;
static BarType_t bar2_with_args_async_call_argument_result;
static void bar2_with_args_async_call_Update(void);

void bar1_no_args_async_call_Update(void)
{
    /* Begin User Code Section: bar1/no_args:update Start */

    /* End User Code Section: bar1/no_args:update Start */
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    AsyncCommand_t command = bar1_no_args_async_call_command;
    bar1_no_args_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar1_no_args_async_call_state = AsyncOperationState_Busy;
            __set_PRIMASK(primask);

            bar_Run_no_args(
                &bar_instance_bar1);

            bar1_no_args_async_call_state = AsyncOperationState_Done;
            break;

        case AsyncCommand_Cancel:
            __set_PRIMASK(primask);
            bar1_no_args_async_call_state = AsyncOperationState_Idle;
            break;

        default:
            __set_PRIMASK(primask);
            break;
    }
    /* Begin User Code Section: bar1/no_args:update End */

    /* End User Code Section: bar1/no_args:update End */
}

void bar1_with_args_async_call_Update(void)
{
    /* Begin User Code Section: bar1/with_args:update Start */

    /* End User Code Section: bar1/with_args:update Start */
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    AsyncCommand_t command = bar1_with_args_async_call_command;
    bar1_with_args_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar1_with_args_async_call_state = AsyncOperationState_Busy;
            __set_PRIMASK(primask);

            bar_Run_with_args(
                &bar_instance_bar1,
                bar1_with_args_async_call_argument_arg,
                &bar1_with_args_async_call_argument_result);

            bar1_with_args_async_call_state = AsyncOperationState_Done;
            break;

        case AsyncCommand_Cancel:
            __set_PRIMASK(primask);
            bar1_with_args_async_call_state = AsyncOperationState_Idle;
            break;

        default:
            __set_PRIMASK(primask);
            break;
    }
    /* Begin User Code Section: bar1/with_args:update End */

    /* End User Code Section: bar1/with_args:update End */
}

void bar2_no_args_async_call_Update(void)
{
    /* Begin User Code Section: bar2/no_args:update Start */

    /* End User Code Section: bar2/no_args:update Start */
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    AsyncCommand_t command = bar2_no_args_async_call_command;
    bar2_no_args_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar2_no_args_async_call_state = AsyncOperationState_Busy;
            __set_PRIMASK(primask);

            bar_Run_no_args(
                &bar_instance_bar2);

            bar2_no_args_async_call_state = AsyncOperationState_Done;
            break;

        case AsyncCommand_Cancel:
            __set_PRIMASK(primask);
            bar2_no_args_async_call_state = AsyncOperationState_Idle;
            break;

        default:
            __set_PRIMASK(primask);
            break;
    }
    /* Begin User Code Section: bar2/no_args:update End */

    /* End User Code Section: bar2/no_args:update End */
}

void bar2_with_args_async_call_Update(void)
{
    /* Begin User Code Section: bar2/with_args:update Start */

    /* End User Code Section: bar2/with_args:update Start */
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    AsyncCommand_t command = bar2_with_args_async_call_command;
    bar2_with_args_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar2_with_args_async_call_state = AsyncOperationState_Busy;
            __set_PRIMASK(primask);

            bar_Run_with_args(
                &bar_instance_bar2,
                bar2_with_args_async_call_argument_arg,
                &bar2_with_args_async_call_argument_result);

            bar2_with_args_async_call_state = AsyncOperationState_Done;
            break;

        case AsyncCommand_Cancel:
            __set_PRIMASK(primask);
            bar2_with_args_async_call_state = AsyncOperationState_Idle;
            break;

        default:
            __set_PRIMASK(primask);
            break;
    }
    /* Begin User Code Section: bar2/with_args:update End */

    /* End User Code Section: bar2/with_args:update End */
}

void Runtime_RaiseEvent_loop(void)
{
    /* Begin User Code Section: Runtime/loop:run Start */

    /* End User Code Section: Runtime/loop:run Start */
    bar1_no_args_async_call_Update();
    bar1_with_args_async_call_Update();
    bar2_no_args_async_call_Update();
    bar2_with_args_async_call_Update();
    /* Begin User Code Section: Runtime/loop:run End */

    /* End User Code Section: Runtime/loop:run End */
}

AsyncOperationState_t foo_Async_no_args_Call(foo_Instance_t* instance)
{
    /* Begin User Code Section: foo/no_args:async_call Start */

    /* End User Code Section: foo/no_args:async_call Start */
    if (instance == &foo_instance_foo1)
    {
        AsyncOperationState_t returned_state = AsyncOperationState_Busy;
        bar1_no_args_async_call_command = AsyncCommand_None;
        uint32_t primask = __get_PRIMASK();
        __disable_irq();
        if (bar1_no_args_async_call_state == AsyncOperationState_Idle || bar1_no_args_async_call_state == AsyncOperationState_Done)
        {
            bar1_no_args_async_call_state = AsyncOperationState_Started;
            __set_PRIMASK(primask);


            returned_state = AsyncOperationState_Started;
            bar1_no_args_async_call_command = AsyncCommand_Start;
        }
        else
        {
            __set_PRIMASK(primask);
        }
        return returned_state;
    }
    if (instance == &foo_instance_foo2)
    {
        AsyncOperationState_t returned_state = AsyncOperationState_Busy;
        bar2_no_args_async_call_command = AsyncCommand_None;
        uint32_t primask = __get_PRIMASK();
        __disable_irq();
        if (bar2_no_args_async_call_state == AsyncOperationState_Idle || bar2_no_args_async_call_state == AsyncOperationState_Done)
        {
            bar2_no_args_async_call_state = AsyncOperationState_Started;
            __set_PRIMASK(primask);


            returned_state = AsyncOperationState_Started;
            bar2_no_args_async_call_command = AsyncCommand_Start;
        }
        else
        {
            __set_PRIMASK(primask);
        }
        return returned_state;
    }
    /* Begin User Code Section: foo/no_args:async_call End */

    /* End User Code Section: foo/no_args:async_call End */
    return AsyncOperationState_Busy;
}

AsyncOperationState_t foo_Async_no_args_GetResult(foo_Instance_t* instance)
{
    /* Begin User Code Section: foo/no_args:get_result Start */

    /* End User Code Section: foo/no_args:get_result Start */
    if (instance == &foo_instance_foo1)
    {
        AsyncOperationState_t returned_state;
        uint32_t primask = __get_PRIMASK();
        __disable_irq();
        switch (bar1_no_args_async_call_state)
        {
            case AsyncOperationState_Done:
                bar1_no_args_async_call_state = AsyncOperationState_Idle;
                __set_PRIMASK(primask);
                returned_state = AsyncOperationState_Done;
                break;

            case AsyncOperationState_Started:
                __set_PRIMASK(primask);
                returned_state = AsyncOperationState_Busy;
                break;

            default:
                __set_PRIMASK(primask);
                returned_state = bar1_no_args_async_call_state;
                break;
        }
        return returned_state;
    }
    if (instance == &foo_instance_foo2)
    {
        AsyncOperationState_t returned_state;
        uint32_t primask = __get_PRIMASK();
        __disable_irq();
        switch (bar2_no_args_async_call_state)
        {
            case AsyncOperationState_Done:
                bar2_no_args_async_call_state = AsyncOperationState_Idle;
                __set_PRIMASK(primask);
                returned_state = AsyncOperationState_Done;
                break;

            case AsyncOperationState_Started:
                __set_PRIMASK(primask);
                returned_state = AsyncOperationState_Busy;
                break;

            default:
                __set_PRIMASK(primask);
                returned_state = bar2_no_args_async_call_state;
                break;
        }
        return returned_state;
    }
    /* Begin User Code Section: foo/no_args:get_result End */

    /* End User Code Section: foo/no_args:get_result End */
    return AsyncOperationState_Busy;
}

void foo_Async_no_args_Cancel(foo_Instance_t* instance)
{
    /* Begin User Code Section: foo/no_args:cancel Start */

    /* End User Code Section: foo/no_args:cancel Start */
    if (instance == &foo_instance_foo1)
    {
        bar1_no_args_async_call_command = AsyncCommand_Cancel;
    }
    if (instance == &foo_instance_foo2)
    {
        bar2_no_args_async_call_command = AsyncCommand_Cancel;
    }
    /* Begin User Code Section: foo/no_args:cancel End */

    /* End User Code Section: foo/no_args:cancel End */
}

AsyncOperationState_t foo_Async_with_args_Call(foo_Instance_t* instance, uint32_t arg)
{
    /* Begin User Code Section: foo/with_args:async_call Start */

    /* End User Code Section: foo/with_args:async_call Start */
    if (instance == &foo_instance_foo1)
    {
        AsyncOperationState_t returned_state = AsyncOperationState_Busy;
        bar1_with_args_async_call_command = AsyncCommand_None;
        uint32_t primask = __get_PRIMASK();
        __disable_irq();
        if (bar1_with_args_async_call_state == AsyncOperationState_Idle || bar1_with_args_async_call_state == AsyncOperationState_Done)
        {
            bar1_with_args_async_call_state = AsyncOperationState_Started;
            __set_PRIMASK(primask);

            bar1_with_args_async_call_argument_arg = arg;

            returned_state = AsyncOperationState_Started;
            bar1_with_args_async_call_command = AsyncCommand_Start;
        }
        else
        {
            __set_PRIMASK(primask);
        }
        return returned_state;
    }
    if (instance == &foo_instance_foo2)
    {
        AsyncOperationState_t returned_state = AsyncOperationState_Busy;
        bar2_with_args_async_call_command = AsyncCommand_None;
        uint32_t primask = __get_PRIMASK();
        __disable_irq();
        if (bar2_with_args_async_call_state == AsyncOperationState_Idle || bar2_with_args_async_call_state == AsyncOperationState_Done)
        {
            bar2_with_args_async_call_state = AsyncOperationState_Started;
            __set_PRIMASK(primask);

            bar2_with_args_async_call_argument_arg = arg;

            returned_state = AsyncOperationState_Started;
            bar2_with_args_async_call_command = AsyncCommand_Start;
        }
        else
        {
            __set_PRIMASK(primask);
        }
        return returned_state;
    }
    /* Begin User Code Section: foo/with_args:async_call End */

    /* End User Code Section: foo/with_args:async_call End */
    return AsyncOperationState_Busy;
}

AsyncOperationState_t foo_Async_with_args_GetResult(foo_Instance_t* instance, BarType_t* result)
{
    /* Begin User Code Section: foo/with_args:get_result Start */

    /* End User Code Section: foo/with_args:get_result Start */
    if (instance == &foo_instance_foo1)
    {
        AsyncOperationState_t returned_state;
        uint32_t primask = __get_PRIMASK();
        __disable_irq();
        switch (bar1_with_args_async_call_state)
        {
            case AsyncOperationState_Done:
                if (result)
                {
                    *result = bar1_with_args_async_call_argument_result;
                }
                bar1_with_args_async_call_state = AsyncOperationState_Idle;
                __set_PRIMASK(primask);
                returned_state = AsyncOperationState_Done;
                break;

            case AsyncOperationState_Started:
                __set_PRIMASK(primask);
                returned_state = AsyncOperationState_Busy;
                break;

            default:
                __set_PRIMASK(primask);
                returned_state = bar1_with_args_async_call_state;
                break;
        }
        return returned_state;
    }
    if (instance == &foo_instance_foo2)
    {
        AsyncOperationState_t returned_state;
        uint32_t primask = __get_PRIMASK();
        __disable_irq();
        switch (bar2_with_args_async_call_state)
        {
            case AsyncOperationState_Done:
                if (result)
                {
                    *result = bar2_with_args_async_call_argument_result;
                }
                bar2_with_args_async_call_state = AsyncOperationState_Idle;
                __set_PRIMASK(primask);
                returned_state = AsyncOperationState_Done;
                break;

            case AsyncOperationState_Started:
                __set_PRIMASK(primask);
                returned_state = AsyncOperationState_Busy;
                break;

            default:
                __set_PRIMASK(primask);
                returned_state = bar2_with_args_async_call_state;
                break;
        }
        return returned_state;
    }
    /* Begin User Code Section: foo/with_args:get_result End */

    /* End User Code Section: foo/with_args:get_result End */
    return AsyncOperationState_Busy;
}

void foo_Async_with_args_Cancel(foo_Instance_t* instance)
{
    /* Begin User Code Section: foo/with_args:cancel Start */

    /* End User Code Section: foo/with_args:cancel Start */
    if (instance == &foo_instance_foo1)
    {
        bar1_with_args_async_call_command = AsyncCommand_Cancel;
    }
    if (instance == &foo_instance_foo2)
    {
        bar2_with_args_async_call_command = AsyncCommand_Cancel;
    }
    /* Begin User Code Section: foo/with_args:cancel End */

    /* End User Code Section: foo/with_args:cancel End */
}
