#include "runtime.h"
#include "utils.h"
#include "utils_assert.h"

/* Begin User Code Section: Declarations */

/* End User Code Section: Declarations */
static uint8_t foo_DataOutput_queue[8u];
static size_t foo_DataOutput_queue_count = 0u;
static size_t foo_DataOutput_queue_write_index = 0u;
static bool foo_DataOutput_queue_overflow = false;
static uint8_t foo_DataOutput_queue1[16u];
static size_t foo_DataOutput_queue1_count = 0u;
static size_t foo_DataOutput_queue1_write_index = 0u;
static bool foo_DataOutput_queue1_overflow = false;

void foo_Write_DataOutput(uint8_t value)
{
    /* Begin User Code Section: foo/DataOutput:write Start */

    /* End User Code Section: foo/DataOutput:write Start */
    if (foo_DataOutput_queue_count < 8u)
    {
        ++foo_DataOutput_queue_count;
    }
    else
    {
        foo_DataOutput_queue_overflow = true;
    }
    size_t foo_DataOutput_queue_idx = foo_DataOutput_queue_write_index;
    foo_DataOutput_queue_write_index = (foo_DataOutput_queue_write_index + 1u) % 8u;
    foo_DataOutput_queue[foo_DataOutput_queue_idx] = value;
    if (foo_DataOutput_queue1_count < 16u)
    {
        ++foo_DataOutput_queue1_count;
    }
    else
    {
        foo_DataOutput_queue1_overflow = true;
    }
    size_t foo_DataOutput_queue1_idx = foo_DataOutput_queue1_write_index;
    foo_DataOutput_queue1_write_index = (foo_DataOutput_queue1_write_index + 1u) % 16u;
    foo_DataOutput_queue1[foo_DataOutput_queue1_idx] = value;
    /* Begin User Code Section: foo/DataOutput:write End */

    /* End User Code Section: foo/DataOutput:write End */
}

QueueStatus_t foo_Read_QueuedInput1(uint8_t* value)
{
    ASSERT(value != NULL);
    /* Begin User Code Section: foo/QueuedInput1:read Start */

    /* End User Code Section: foo/QueuedInput1:read Start */
    if (foo_DataOutput_queue_count > 0u)
    {
        size_t idx = (foo_DataOutput_queue_write_index - foo_DataOutput_queue_count) % 8u;
        --foo_DataOutput_queue_count;
        *value = foo_DataOutput_queue[idx];

        if (foo_DataOutput_queue_overflow)
        {
            foo_DataOutput_queue_overflow = false;
            return QueueStatus_Overflow;
        }
        else
        {
            return QueueStatus_Ok;
        }
    }
    /* Begin User Code Section: foo/QueuedInput1:read End */

    /* End User Code Section: foo/QueuedInput1:read End */
    return QueueStatus_Empty;
}

QueueStatus_t foo_Read_QueuedInput2(uint8_t* value)
{
    ASSERT(value != NULL);
    /* Begin User Code Section: foo/QueuedInput2:read Start */

    /* End User Code Section: foo/QueuedInput2:read Start */
    if (foo_DataOutput_queue1_count > 0u)
    {
        size_t idx = (foo_DataOutput_queue1_write_index - foo_DataOutput_queue1_count) % 16u;
        --foo_DataOutput_queue1_count;
        *value = foo_DataOutput_queue1[idx];

        if (foo_DataOutput_queue1_overflow)
        {
            foo_DataOutput_queue1_overflow = false;
            return QueueStatus_Overflow;
        }
        else
        {
            return QueueStatus_Ok;
        }
    }
    /* Begin User Code Section: foo/QueuedInput2:read End */

    /* End User Code Section: foo/QueuedInput2:read End */
    return QueueStatus_Empty;
}
