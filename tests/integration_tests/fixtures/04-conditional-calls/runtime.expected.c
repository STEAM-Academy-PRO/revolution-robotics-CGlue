#include "runtime.h"
#include "utils.h"

static foo_Instance_t foo_instance_foo1;
/* Begin User Code Section: Declarations */

/* End User Code Section: Declarations */

void bar_Call_call(uint32_t idx, uint32_t* data)
{
    /* Begin User Code Section: bar/call:run Start */

    /* End User Code Section: bar/call:run Start */
    if (idx == 0)
    {
        foo_Run_run(&foo_instance_foo1, 42, data);
    }
    /* Begin User Code Section: bar/call:run End */

    /* End User Code Section: bar/call:run End */
}
