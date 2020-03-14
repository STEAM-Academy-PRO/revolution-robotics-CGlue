#include "runtime.h"
#include "utils.h"

static foo_Instance_t foo_instance_foo1;

void bar_Call_call(uint32_t idx, uint32_t* data)
{
    if (idx == 0)
    {
        foo_Run_run(&foo_instance_foo1, 42, data);
    }
}
