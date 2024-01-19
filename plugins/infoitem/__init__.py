from sopel import plugin

PLUGIN_NAME = 'infoitem'

# TODO: plugin.require_bot_privilege


@plugin.rule(r'^!(?P<item>.+?)\s*(?P<explicit>\?)?$')
def get_values(bot, trigger):
    item = trigger.group('item')

    values = bot.db.get_plugin_value(PLUGIN_NAME, item)
    if values:
        bot.say(f'{item} is {" .. ".join(values)}')
    elif trigger.group('explicit'):
        bot.say(f'Nothing known about {item}')

@plugin.rule(r'^!(?P<item>.+?)\s*=\s*(?P<value>.+?)\s*$')
def add_value(bot, trigger):
    item = trigger.group('item')
    value = trigger.group('value')

    values = bot.db.get_plugin_value(PLUGIN_NAME, item)
    if values:
        if value in values:
            return
        values.append(value)
    else:
        values = [value]
    bot.db.set_plugin_value(PLUGIN_NAME, item, values)

@plugin.command('forget')
def forget(bot, trigger):
    arguments = trigger.group(2)
    if not arguments:
        bot.reply('Forget what?')
        return

    parts = arguments.split(None, 1)
    item = parts[0]
    try:
        to_forget = parts[1]
    except IndexError:
        bot.db.delete_plugin_value(PLUGIN_NAME, item)
    else:
        values = bot.db.get_plugin_value(PLUGIN_NAME, item)
        # TODO: partial matches
        values = [value for value in values if value not in to_forget]
        bot.db.set_plugin_value(PLUGIN_NAME, item, values)
