#include "runtime.h"
#include "utils.h"

static foo_Instance_t foo_instance_foo1;
static foo_Instance_t foo_instance_foo2;
static uint32_t foo1_WPort_variable = 0u;
static uint32_t foo2_WPort_variable = 0u;

void Runtime_RaiseEvent_OnInit(void)
{
    foo_Run_Runnable(&foo_instance_foo1, 5);
    foo_Run_Runnable(&foo_instance_foo2, 6);
}

void foo_Write_WPort(foo_Instance_t* instance, uint32_t value)
{
    if (instance == &foo_instance_foo1)
    {
        foo1_WPort_variable = value;
    }
    if (instance == &foo_instance_foo2)
    {
        foo2_WPort_variable = value;
    }
}

uint32_t foo_Read_RPort(foo_Instance_t* instance)
{
    uint32_t return_value;
    if (instance == &foo_instance_foo2)
    {
        return_value = foo1_WPort_variable;
    }
    if (instance == &foo_instance_foo1)
    {
        return_value = foo2_WPort_variable;
    }
    return return_value;
}
