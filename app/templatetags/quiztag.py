from django import template

register = template.Library()

@register.inclusion_tag('right_answer.html', takes_context=True)
def right_answer_for_all(context, question):
    answers=question.get_answers()
    wrong_list=context.get('wrong_answers', [])
    if question.id in wrong_list:
        user_was_wrong = True
    else:
         user_was_wrong=False
    return{
        'previous':{'answers': answers},
        'user_was_wrong': user_was_wrong}
@register.filter
def ansChoice_string(quetion, answer):
    return question.ansChoice_string(answer)
