import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open('players.json', 'r') as file:
        players = json.load(file)

    for player in players:
        race_info = player.get('race', {})
        race, _ = Race.objects.get_or_create(
            name=race_info.get('name'),
            defaults={'description': race_info.get('description', '')}
        )
        guild_info = player.get('guild', {})
        guild_name = guild_info.get('name')
        guild = None
        if guild_name:
            guild, _ = Guild.objects.get_or_create(
                name=guild_name,
                defaults={'description': guild_info.get('description', '')}
            )
        for skill_data in player.get('skills', []):
            Skill.objects.get_or_create(
                name=skill_data.get('name'),
                race=race,
                defaults={'bonus': skill_data.get('bonus', '')}
            )
        Player.objects.get_or_create(
            nickname=player['nickname'],
            defaults={
                'email': player.get('email', ''),
                'bio': player.get('bio', ''),
                'race': race,
                'guild': guild
            }
        )


if __name__ == "__main__":
    main()
