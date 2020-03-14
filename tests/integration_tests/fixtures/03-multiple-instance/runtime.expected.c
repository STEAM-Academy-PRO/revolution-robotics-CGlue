#include "runtime.h"
#include "utils.h"
#include "utils_assert.h"

static foo_Instance_t foo_instance_foo1;
static foo_Instance_t foo_instance_foo2;
static uint32_t foo1_WPort_variable = 0u;
static uint32_t foo1_WPort_queue[2u];
static size_t foo1_WPort_queue_count = 0u;
static size_t foo1_WPort_queue_write_index = 0u;
static bool foo1_WPort_queue_overflow = false;
static uint32_t foo2_WPort_queue;
static bool foo2_WPort_queue_overflow = false;
static bool foo2_WPort_queue_data_valid = false;
static uint32_t foo2_WPort_variable = 0u;
static uint32_t foo1_WIPort_array[3] = { 0u, 0u, 0u };
static uint32_t foo2_WIPort_array[3] = { 0u, 0u, 0u };

void Runtime_RaiseEvent_OnInit(void)
{
    foo_Run_Runnable(&foo_instance_foo1, 5);
    foo_Run_Runnable(&foo_instance_foo2, 6);
}

void foo_RaiseEvent_EventPort(foo_Instance_t* instance, uint32_t arg1)
{
    if (instance == &foo_instance_foo1)
    {
        foo_Run_Runnable(&foo_instance_foo2, arg1);
    }
    if (instance == &foo_instance_foo2)
    {
        foo_Run_Runnable(&foo_instance_foo1, arg1);
    }
}

uint32_t foo_Call_CallPort(foo_Instance_t* instance, uint32_t arg1)
{
    if (instance == &foo_instance_foo1)
    {
        return foo_Run_RunnableWithReturnValue(&foo_instance_foo2, arg1);
    }
    if (instance == &foo_instance_foo2)
    {
        return foo_Run_RunnableWithReturnValue(&foo_instance_foo1, arg1);
    }
    return 0u;
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
    if (instance == &foo_instance_foo1)
    {
        if (foo1_WPort_queue_count < 2u)
        {
            ++foo1_WPort_queue_count;
        }
        else
        {
            foo1_WPort_queue_overflow = true;
        }
        size_t idx = foo1_WPort_queue_write_index;
        foo1_WPort_queue_write_index = (foo1_WPort_queue_write_index + 1u) % 2u;
        foo1_WPort_queue[idx] = value;
    }
    if (instance == &foo_instance_foo2)
    {
        foo2_WPort_queue_overflow = foo2_WPort_queue_data_valid;
        foo2_WPort_queue = value;
        foo2_WPort_queue_data_valid = true;
    }
    if (instance == &foo_instance_foo2)
    {
        foo2_WPort_variable = value;
    }
}

uint32_t foo_Read_RCAPort(foo_Instance_t* instance, uint32_t index)
{
    ASSERT(index < 3);
    if (instance == &foo_instance_foo2)
    {
        return foo_Constant_CAPort(&foo_instance_foo2, index);
    }
    if (instance == &foo_instance_foo1)
    {
        return foo_Constant_CAPort(&foo_instance_foo1, index);
    }
    return 0u;
}

uint32_t foo_Read_RCPort(foo_Instance_t* instance)
{
    if (instance == &foo_instance_foo2)
    {
        return foo_Constant_CPort(&foo_instance_foo2);
    }
    if (instance == &foo_instance_foo1)
    {
        return foo_Constant_CPort(&foo_instance_foo1);
    }
    return 0u;
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

QueueStatus_t foo_Read_RQPort(foo_Instance_t* instance, uint32_t* value)
{
    ASSERT(value != NULL);
    if (instance == &foo_instance_foo1)
    {
        if (foo1_WPort_queue_count > 0u)
        {
            size_t idx = (foo1_WPort_queue_write_index - foo1_WPort_queue_count) % 2u;
            --foo1_WPort_queue_count;
            *value = foo1_WPort_queue[idx];

            if (foo1_WPort_queue_overflow)
            {
                foo1_WPort_queue_overflow = false;
                return QueueStatus_Overflow;
            }
            else
            {
                return QueueStatus_Ok;
            }
        }
    }
    if (instance == &foo_instance_foo2)
    {
        bool was_overflow = foo2_WPort_queue_overflow;
        if (foo2_WPort_queue_data_valid)
        {
            foo2_WPort_queue_overflow = false;
            *value = foo2_WPort_queue;
            foo2_WPort_queue_data_valid = false;
            if (was_overflow)
            {
                return QueueStatus_Overflow;
            }
            else
            {
                return QueueStatus_Ok;
            }
        }
    }
    return QueueStatus_Empty;
}
