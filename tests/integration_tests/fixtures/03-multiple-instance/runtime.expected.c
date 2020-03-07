#include "runtime.h"
#include "utils.h"
#include "utils_assert.h"

static foo_Instance_t foo_instance_foo1;
static foo_Instance_t foo_instance_foo2;
static uint32_t foo1_WPort_variable = 0u;
static uint32_t foo2_WPort_variable = 0u;
static uint32_t foo1_WIPort_array[3] = { 0u, 0u, 0u };
static uint32_t foo2_WIPort_array[3] = { 0u, 0u, 0u };

void Runtime_RaiseEvent_OnInit(void)
{
    foo_Run_Runnable(&foo_instance_foo1, 5);
    foo_Run_Runnable(&foo_instance_foo2, 6);
}

void foo_Write_WIPort(foo_Instance_t* instance, uint32_t index, uint32_t value)
{
    ASSERT(index < 3);
    if (instance == &foo_instance_foo1)
    {
        foo1_WIPort_array[index] = value;
    }
    if (instance == &foo_instance_foo2)
    {
        foo2_WIPort_array[index] = value;
    }
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

uint32_t foo_Read_RIPort(foo_Instance_t* instance, uint32_t index)
{
    ASSERT(index < 3);
    if (instance == &foo_instance_foo2)
    {
        return foo1_WIPort_array[index];
    }
    if (instance == &foo_instance_foo1)
    {
        return foo2_WIPort_array[index];
    }
    return 0u;
}

uint32_t foo_Read_RPort(foo_Instance_t* instance)
{
    if (instance == &foo_instance_foo2)
    {
        return foo1_WPort_variable;
    }
    if (instance == &foo_instance_foo1)
    {
        return foo2_WPort_variable;
    }
    return 0u;
}

uint32_t foo_Read_RPortFromI(foo_Instance_t* instance)
{
    if (instance == &foo_instance_foo2)
    {
        return foo1_WIPort_array[2];
    }
    if (instance == &foo_instance_foo1)
    {
        return foo2_WIPort_array[3];
    }
    return 0u;
}
