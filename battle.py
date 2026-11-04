import ex3


def test_factory(factory: ex3.CreatureFactory) -> None:
    print("Testing Factory")
    if isinstance(factory, ex3.FlameFactory):
        bs_entity = factory.create_base()
        ev_entity = factory.create_evolved()
        print(bs_entity.describe())
        print(bs_entity.attack())
        print(ev_entity.describe())
        print(ev_entity.attack())
    elif isinstance(factory, ex3.TransformCreatureFactory):
        bs_entity = factory.create_base()
        ev_entity = factory.create_evolved()
        print(bs_entity.describe())
        print(bs_entity.attack())
        print(ev_entity.describe())
        print(ev_entity.attack())


def test_battle(fct_1: ex3.CreatureFactory,
                fct_2: ex3.CreatureFactory) -> None:
    print("Testing battle")
    bs_fct_1 = fct_1.create_base()
    bs_fct_2 = fct_2.create_base()
    print(bs_fct_1.describe())
    print("\tvs.")
    print(bs_fct_2.describe())
    print("\tfight!")
    print(bs_fct_1.attack())
    print(bs_fct_2.attack())


def main() -> None:
    fl_factory = ex3.FlameFactory()
    trns_factory = ex3.TransformCreatureFactory()
    test_factory(fl_factory)
    print()
    test_factory(trns_factory)
    print()
    test_battle(fl_factory, trns_factory)


if __name__ == "__main__":
    main()
