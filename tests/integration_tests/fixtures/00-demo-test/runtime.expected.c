#include "runtime.h"
#include "utils.h"

/* Begin User Code Section: Declarations */
some user code
/* End User Code Section: Declarations */

void Runtime_RaiseEvent_OnInit(void)
{
    /* Begin User Code Section: Runtime/OnInit:run Start */
    some other user code
    /* End User Code Section: Runtime/OnInit:run Start */
    foo_Run_Initialize();
    /* Begin User Code Section: Runtime/OnInit:run End */

    /* End User Code Section: Runtime/OnInit:run End */
}

void foo_RaiseEvent_EventSource(void)
{
    /* Begin User Code Section: foo/EventSource:run Start */

    /* End User Code Section: foo/EventSource:run Start */
    foo_Run_EventHandler(2);
    /* Begin User Code Section: foo/EventSource:run End */

    /* End User Code Section: foo/EventSource:run End */
}
