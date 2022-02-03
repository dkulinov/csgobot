from Commons.Types.MatchType import MatchType


def get_embed_author_title(author) -> str:
    return f'hey {author}, here you go!'


def mapToMatchType(match_filter: str) -> MatchType:
    if match_filter.lower() == "top_tier":
        return MatchType.TopTier
    elif match_filter.lower() == "lan":
        return MatchType.LanOnly
    elif match_filter.lower() == "none":
        return MatchType.Default
    else:
        raise TypeError("Filter has to be either top_tier or lan")
