/*
 * merge.c
 *
 *  Created on: 2017年12月11日
 *      Author:anlang
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>

struct node
{
	int value;
	struct node* next;
};

struct node* merge(struct node*a,struct node*b)
{
	struct node* new_list_head = b;
	struct node* tmp = b;
	struct node* need_merge = a;

	if(!a)
	{
		return b;
	}

	if(!b)
	{
		return a;
	}

	if(a->value <= b->value)
	{
		new_list_head = a;
		tmp = a;
		need_merge = b;
	}

	while(1)
	{
		if(tmp->next)
		{
			if(!need_merge)
			{
				return new_list_head;
			}
			else
			{
				if(tmp->next->value >= need_merge->value)
				{
					struct node* node = need_merge;
					need_merge = need_merge->next;//move to next node
					node->next = tmp->next;//delete node from need_merged
					tmp->next = node;//tmp---node---tmp->next
					//tmp stand here
				}
				else
				{
					tmp = tmp->next;
				}
			}
		}
		else
		{
			tmp->next = need_merge;
			return new_list_head;
		}
	}
}


int main(int argc,char**argv)
{
	struct node a ={
			.value = 3,
			.next = NULL
	};

	struct node b = {
			.value = 2,
			.next = NULL
	};

	struct node c = {
			.value=1,
			.next = &a
	};
	//testcase 0
	assert(merge(NULL,NULL) == NULL);
	//testcase 1
	assert(merge(&a,NULL) == &a);
	//testcase 2
	assert(merge(NULL,&b) == &b);
	//testcase 3
	assert(merge(&a,&b) == &b);
	b.next = NULL;
	//testcase 4
	assert(merge(&c,&b) == &c);
	assert(c.next == &b);
	assert(c.next->next == &a);
	return 0;
}
