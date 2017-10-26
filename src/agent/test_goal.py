import unittest

from goal import *

class GoalModelTest(unittest.TestCase):
    def test_get_available_tasks(self):
        goal = {'goal': 'introduce myself',
             'require': [
                ['say', {'words':'hello'}],
                {'goal': 'say hello',
                 'require': [
                    ['say', {'words':'myname'}],
                    ['say', {'words':'hehe'}],
                     {'goal': 'say hajime',
                      'require': [
                        ['say', {'words':'hajime'}]
                       ]}
                  ]
                }
             ]
        }
        model = create_goal_set(goal)
        result = model.get_available_tasks()
        expected_result = Task('say', {'words':'hajime'})
        self.assertEqual(expected_result.arguments, result[0].arguments)

    # test the get_goal() function which returns its first subgoals(subgoals[0]).
    def test_get_goal(self):
        goal = {'goal': 'introduce myself',
             'require': [
                ['say', {'words':'hello'}],
                {'goal': 'say hello',
                 'require': [
                    ['say', {'words':'myname'}],
                    ['say', {'words':'hehe'}],
                     {'goal': 'say hajime',
                      'require': [
                        ['say', {'words':'hajime'}]
                       ]}
                  ]
                }
             ]
        }
        model = create_goal_set(goal)
        result = model.get_goal().name
        expected_result = "say hello"
        self.assertEqual(expected_result, result) # checked the goal's subgoal name("say hello")





if __name__ == '__main__':
    unittest.main()
