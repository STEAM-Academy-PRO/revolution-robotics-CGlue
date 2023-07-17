#include "runtime.h"
#include "utils.h"

/* Begin User Code Section: Declarations */

/* End User Code Section: Declarations */

/* bar_no_args_async_call */
static AsyncOperationState_t bar_no_args_async_call_state = AsyncOperationState_Idle;
static AsyncCommand_t bar_no_args_async_call_command = AsyncCommand_None;
static void bar_no_args_async_call_Update(void);

/* bar_async_runnable_async_call */
static AsyncOperationState_t bar_async_runnable_async_call_state = AsyncOperationState_Idle;
static AsyncCommand_t bar_async_runnable_async_call_command = AsyncCommand_None;
static uint32_t bar_async_runnable_async_call_argument_arg;
static void bar_async_runnable_async_call_Update(void);

/* bar_with_args_async_call */
static AsyncOperationState_t bar_with_args_async_call_state = AsyncOperationState_Idle;
static AsyncCommand_t bar_with_args_async_call_command = AsyncCommand_None;
static uint32_t bar_with_args_async_call_argument_arg;
static BarType_t bar_with_args_async_call_argument_result;
static void bar_with_args_async_call_Update(void);

void bar_no_args_async_call_Update(void)
{
    /* Begin User Code Section: bar/no_args:update Start */

    /* End User Code Section: bar/no_args:update Start */
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    AsyncCommand_t command = bar_no_args_async_call_command;
    bar_no_args_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar_no_args_async_call_state = AsyncOperationState_Busy;
            __set_PRIMASK(primask);

            bar_Run_no_args();

            bar_no_args_async_call_state = AsyncOperationState_Done;
            break;

        case AsyncCommand_Cancel:
            __set_PRIMASK(primask);
            bar_no_args_async_call_state = AsyncOperationState_Idle;
            break;

        default:
            __set_PRIMASK(primask);
            break;
    }
    /* Begin User Code Section: bar/no_args:update End */

    /* End User Code Section: bar/no_args:update End */
}

void bar_with_args_async_call_Update(void)
{
    /* Begin User Code Section: bar/with_args:update Start */

    /* End User Code Section: bar/with_args:update Start */
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    AsyncCommand_t command = bar_with_args_async_call_command;
    bar_with_args_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar_with_args_async_call_state = AsyncOperationState_Busy;
            __set_PRIMASK(primask);

            bar_Run_with_args(
                bar_with_args_async_call_argument_arg,
                &bar_with_args_async_call_argument_result);

            bar_with_args_async_call_state = AsyncOperationState_Done;
            break;

        case AsyncCommand_Cancel:
            __set_PRIMASK(primask);
            bar_with_args_async_call_state = AsyncOperationState_Idle;
            break;

        default:
            __set_PRIMASK(primask);
            break;
    }
    /* Begin User Code Section: bar/with_args:update End */

    /* End User Code Section: bar/with_args:update End */
}

void Runtime_RaiseEvent_loop(void)
{
    /* Begin User Code Section: Runtime/loop:run Start */

    /* End User Code Section: Runtime/loop:run Start */
    bar_no_args_async_call_Update();
    bar_async_runnable_async_call_Update();
    bar_with_args_async_call_Update();
    /* Begin User Code Section: Runtime/loop:run End */

    /* End User Code Section: Runtime/loop:run End */
}

AsyncOperationState_t foo_Async_no_args_Call(void)
{
    /* Begin User Code Section: foo/no_args:async_call Start */

    /* End User Code Section: foo/no_args:async_call Start */
    AsyncOperationState_t returned_state = AsyncOperationState_Busy;
    bar_no_args_async_call_command = AsyncCommand_None;
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    if (bar_no_args_async_call_state == AsyncOperationState_Idle || bar_no_args_async_call_state == AsyncOperationState_Done)
    {
        bar_no_args_async_call_state = AsyncOperationState_Started;
        __set_PRIMASK(primask);


        returned_state = AsyncOperationState_Started;
        bar_no_args_async_call_command = AsyncCommand_Start;
    }
    else
    {
        __set_PRIMASK(primask);
    }
    return returned_state;
    /* Begin User Code Section: foo/no_args:async_call End */

    /* End User Code Section: foo/no_args:async_call End */
}

AsyncOperationState_t foo_Async_no_args_GetResult(void)
{
    /* Begin User Code Section: foo/no_args:get_result Start */

    /* End User Code Section: foo/no_args:get_result Start */
    AsyncOperationState_t returned_state;
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    switch (bar_no_args_async_call_state)
    {
        case AsyncOperationState_Done:
            bar_no_args_async_call_state = AsyncOperationState_Idle;
            __set_PRIMASK(primask);
            returned_state = AsyncOperationState_Done;
            break;

        case AsyncOperationState_Started:
            __set_PRIMASK(primask);
            returned_state = AsyncOperationState_Busy;
            break;

        default:
            __set_PRIMASK(primask);
            returned_state = bar_no_args_async_call_state;
            break;
    }
    return returned_state;
    /* Begin User Code Section: foo/no_args:get_result End */

    /* End User Code Section: foo/no_args:get_result End */
}

void foo_Async_no_args_Cancel(void)
{
    /* Begin User Code Section: foo/no_args:cancel Start */

    /* End User Code Section: foo/no_args:cancel Start */
    bar_no_args_async_call_command = AsyncCommand_Cancel;
    /* Begin User Code Section: foo/no_args:cancel End */

    /* End User Code Section: foo/no_args:cancel End */
}

void bar_async_runnable_async_call_Update(void)
{
    /* Begin User Code Section: bar/async_runnable:update Start */

    /* End User Code Section: bar/async_runnable:update Start */
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    AsyncCommand_t command = bar_async_runnable_async_call_command;
    bar_async_runnable_async_call_command = AsyncCommand_None;

    switch (command)
    {
        case AsyncCommand_Start:
            bar_async_runnable_async_call_state = AsyncOperationState_Busy;
            __set_PRIMASK(primask);

            AsyncResult_t result = bar_AsyncRunnable_async_runnable(command,
                &bar_async_runnable_async_call_argument_arg);
            switch (result)
            {
                case AsyncResult_Ok:
                    bar_async_runnable_async_call_state = AsyncOperationState_Done;
                    break;

                case AsyncResult_Pending:
                    break;

                default:
                    ASSERT(0);
                    break;
            }
            break;

        case AsyncCommand_None:
            if (bar_async_runnable_async_call_state == AsyncOperationState_Busy)
            {
                __set_PRIMASK(primask);

                AsyncResult_t result = bar_AsyncRunnable_async_runnable(command,
                &bar_async_runnable_async_call_argument_arg);
                switch (result)
                {
                    case AsyncResult_Ok:
                        bar_async_runnable_async_call_state = AsyncOperationState_Done;
                        break;

                    case AsyncResult_Pending:
                        break;

                    default:
                        ASSERT(0);
                        break;
                }
            }
            else
            {
                __set_PRIMASK(primask);
            }
            break;

        case AsyncCommand_Cancel:
            if (bar_async_runnable_async_call_state == AsyncOperationState_Busy)
            {
                __set_PRIMASK(primask);
                (void) bar_AsyncRunnable_async_runnable(AsyncCommand_Cancel,
                &bar_async_runnable_async_call_argument_arg);
            }
            else
            {
                __set_PRIMASK(primask);
            }
            bar_async_runnable_async_call_state = AsyncOperationState_Idle;
            break;

        default:
            __set_PRIMASK(primask);
            ASSERT(0);
            break;
    }

    /* Begin User Code Section: bar/async_runnable:update End */

    /* End User Code Section: bar/async_runnable:update End */
}

AsyncOperationState_t foo_Async_no_args_async_Call(void)
{
    /* Begin User Code Section: foo/no_args_async:async_call Start */

    /* End User Code Section: foo/no_args_async:async_call Start */
    AsyncOperationState_t returned_state = AsyncOperationState_Busy;
    bar_async_runnable_async_call_command = AsyncCommand_None;
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    if (bar_async_runnable_async_call_state == AsyncOperationState_Idle || bar_async_runnable_async_call_state == AsyncOperationState_Done)
    {
        bar_async_runnable_async_call_state = AsyncOperationState_Started;
        __set_PRIMASK(primask);


        returned_state = AsyncOperationState_Started;
        bar_async_runnable_async_call_command = AsyncCommand_Start;
    }
    else
    {
        __set_PRIMASK(primask);
    }
    return returned_state;
    /* Begin User Code Section: foo/no_args_async:async_call End */

    /* End User Code Section: foo/no_args_async:async_call End */
}

AsyncOperationState_t foo_Async_no_args_async_GetResult(void)
{
    /* Begin User Code Section: foo/no_args_async:get_result Start */

    /* End User Code Section: foo/no_args_async:get_result Start */
    AsyncOperationState_t returned_state;
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    switch (bar_async_runnable_async_call_state)
    {
        case AsyncOperationState_Done:
            bar_async_runnable_async_call_state = AsyncOperationState_Idle;
            __set_PRIMASK(primask);
            returned_state = AsyncOperationState_Done;
            break;

        case AsyncOperationState_Started:
            __set_PRIMASK(primask);
            returned_state = AsyncOperationState_Busy;
            break;

        default:
            __set_PRIMASK(primask);
            returned_state = bar_async_runnable_async_call_state;
            break;
    }
    return returned_state;
    /* Begin User Code Section: foo/no_args_async:get_result End */

    /* End User Code Section: foo/no_args_async:get_result End */
}

void foo_Async_no_args_async_Cancel(void)
{
    /* Begin User Code Section: foo/no_args_async:cancel Start */

    /* End User Code Section: foo/no_args_async:cancel Start */
    bar_async_runnable_async_call_command = AsyncCommand_Cancel;
    /* Begin User Code Section: foo/no_args_async:cancel End */

    /* End User Code Section: foo/no_args_async:cancel End */
}

AsyncOperationState_t foo_Async_with_args_Call(uint32_t arg)
{
    /* Begin User Code Section: foo/with_args:async_call Start */

    /* End User Code Section: foo/with_args:async_call Start */
    AsyncOperationState_t returned_state = AsyncOperationState_Busy;
    bar_with_args_async_call_command = AsyncCommand_None;
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    if (bar_with_args_async_call_state == AsyncOperationState_Idle || bar_with_args_async_call_state == AsyncOperationState_Done)
    {
        bar_with_args_async_call_state = AsyncOperationState_Started;
        __set_PRIMASK(primask);

        bar_with_args_async_call_argument_arg = arg;

        returned_state = AsyncOperationState_Started;
        bar_with_args_async_call_command = AsyncCommand_Start;
    }
    else
    {
        __set_PRIMASK(primask);
    }
    return returned_state;
    /* Begin User Code Section: foo/with_args:async_call End */

    /* End User Code Section: foo/with_args:async_call End */
}

AsyncOperationState_t foo_Async_with_args_GetResult(BarType_t* result)
{
    /* Begin User Code Section: foo/with_args:get_result Start */

    /* End User Code Section: foo/with_args:get_result Start */
    AsyncOperationState_t returned_state;
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    switch (bar_with_args_async_call_state)
    {
        case AsyncOperationState_Done:
            if (result)
            {
                *result = bar_with_args_async_call_argument_result;
            }
            bar_with_args_async_call_state = AsyncOperationState_Idle;
            __set_PRIMASK(primask);
            returned_state = AsyncOperationState_Done;
            break;

        case AsyncOperationState_Started:
            __set_PRIMASK(primask);
            returned_state = AsyncOperationState_Busy;
            break;

        default:
            __set_PRIMASK(primask);
            returned_state = bar_with_args_async_call_state;
            break;
    }
    return returned_state;
    /* Begin User Code Section: foo/with_args:get_result End */

    /* End User Code Section: foo/with_args:get_result End */
}

void foo_Async_with_args_Cancel(void)
{
    /* Begin User Code Section: foo/with_args:cancel Start */

    /* End User Code Section: foo/with_args:cancel Start */
    bar_with_args_async_call_command = AsyncCommand_Cancel;
    /* Begin User Code Section: foo/with_args:cancel End */

    /* End User Code Section: foo/with_args:cancel End */
}
