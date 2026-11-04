import ex3


def main() -> None:
    bs_entity = ex3.TransformCreatureFactory().create_base()
    ev_entity = ex3.TransformCreatureFactory().create_evolved()
    print("Testing Creature with transform capability")
    print(" base:")
    print(bs_entity.describe())
    print(bs_entity.attack())
    print(bs_entity.transform())
    print(bs_entity.attack())
    print(bs_entity.revert())

    print(" evolved:")
    print(ev_entity.describe())
    print(ev_entity.attack())
    print(ev_entity.transform())
    print(ev_entity.attack())
    print(ev_entity.revert())


if __name__ == "__main__":
    main()
