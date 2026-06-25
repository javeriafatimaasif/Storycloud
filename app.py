from flask import Flask, render_template, jsonify, request
import json, random

app = Flask(__name__)

BOOKS = [
    # === Public Domain Classics ===
    {
        "id": 1,
        "title": "Alice's Adventures in Wonderland",
        "author": "Lewis Carroll",
        "cover_color": "#e8a0bf",
        "accent": "#c2185b",
        "year": 1865,
        "moods": ["whimsical", "adventurous", "curious", "playful"],
        "description": "Follow Alice down the rabbit hole into a world of impossible wonders, talking animals, and delightful absurdity.",
        "pages": [
            {"title": "Chapter I – Down the Rabbit-Hole", "content": "Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, \"and what is the use of a book,\" thought Alice \"without pictures or conversations?\"\n\nSo she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."},
            {"title": "Chapter II – The Pool of Tears", "content": "\"Curiouser and curiouser!\" cried Alice (she was so much surprised, that for the moment she quite forgot how to speak good English); \"now I'm opening out like the largest telescope that ever was! Good-bye, feet!\" (for when she looked down at her feet, they seemed to be almost out of sight, they were getting so far off).\n\n\"Oh, my poor little feet, I wonder who will put on your shoes and stockings for you now, dears? I'm sure I shan't be able! I shall be a great deal too far off to trouble myself about you: you must manage the best way you can.\""},
            {"title": "Chapter III – A Caucus-Race", "content": "They were indeed a queer-looking party that assembled on the bank—the birds with draggled feathers, the animals with their fur clinging close to them, and all dripping wet, cross, and uncomfortable.\n\nThe first question of course was, how to get dry again: they had a consultation about this, and after a few minutes it seemed quite natural to Alice to find herself talking familiarly with them, as if she had known them all her life."},
            {"title": "Chapter IV – The Rabbit Sends in a Little Bill", "content": "It was the White Rabbit, trotting slowly back again, and looking anxiously about as it went, as if it had lost something; and she heard it muttering to itself \"The Duchess! The Duchess! Oh my dear paws! Oh my fur and whiskers! She'll get me executed, as sure as ferrets are ferrets! Where CAN I have dropped them, I wonder?\" Alice guessed in a moment that it was looking for the fan and the pair of white kid gloves, and she very good-naturedly began hunting about for them."},
        ]
    },
    {
        "id": 2,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "cover_color": "#a5d6a7",
        "accent": "#2e7d32",
        "year": 1813,
        "moods": ["romantic", "witty", "social", "classic"],
        "description": "Elizabeth Bennet navigates love, class, and first impressions in Austen's sparkling comedy of manners.",
        "pages": [
            {"title": "Chapter 1", "content": "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.\n\nHowever little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered as the rightful property of some one or other of their daughters."},
            {"title": "Chapter 2", "content": "Mr. Bennet was among the earliest of her visitors, and Mr. Bingley was among the first of those who were introduced to her. He was quite young, wonderfully handsome, extremely agreeable, and to crown the whole, he meant to be at the next assembly with a large party. Nothing could be more delightful! To be fond of dancing was a certain step towards falling in love; and very lively hopes of Mr. Bingley's heart were entertained."},
            {"title": "Chapter 3", "content": "Not all that Mrs. Bennet, however, with the assistance of her five daughters, could ask on the subject was sufficient to draw from her husband any satisfactory description of Mr. Bingley. They attacked him in various ways; with barefaced questions, ingenious suppositions, and distant surmises; but he eluded the skill of them all; and they were at last obliged to accept the second-hand intelligence of their neighbour Lady Lucas."},
        ]
    },
    {
        "id": 3,
        "title": "The Adventures of Sherlock Holmes",
        "author": "Arthur Conan Doyle",
        "cover_color": "#ffe082",
        "accent": "#f57f17",
        "year": 1892,
        "moods": ["mysterious", "curious", "thrilling", "clever"],
        "description": "Follow the world's greatest detective through twelve brilliant investigations of crime, deduction, and Victorian intrigue.",
        "pages": [
            {"title": "A Scandal in Bohemia – Part I", "content": "To Sherlock Holmes she is always THE woman. I have seldom heard him mention her under any other name. In his eyes she eclipses and predominates the whole of her sex. It was not that he felt any emotion akin to love for Irene Adler. All emotions, and that one particularly, were abhorrent to his cold, precise but admirably balanced mind."},
            {"title": "A Scandal in Bohemia – Part II", "content": "I had seen little of Holmes lately. My marriage had drifted us apart. My own complete happiness, and the home-centred interests which rise up around the man who first finds himself master of his own establishment, were sufficient to absorb all my attention, while Holmes, who loathed every form of society with his whole Bohemian soul, remained in our lodgings in Baker Street, buried among his old books, and alternating from week to week between cocaine and ambition."},
            {"title": "The Red-Headed League – Part I", "content": "I had called upon my friend, Mr. Sherlock Holmes, one day in the autumn of last year and found him in deep conversation with a very stout, florid-faced, elderly gentleman with fiery red hair. With an apology for my intrusion, I was about to withdraw when Holmes pulled me abruptly into the room and closed the door behind me.\n\n\"You could not possibly have come at a better time, my dear Watson,\" he said cordially."},
        ]
    },
    {
        "id": 4,
        "title": "Frankenstein",
        "author": "Mary Shelley",
        "cover_color": "#b0bec5",
        "accent": "#37474f",
        "year": 1818,
        "moods": ["dark", "philosophical", "mysterious", "thrilling"],
        "description": "Victor Frankenstein's obsession with creation births a creature that challenges what it means to be human.",
        "pages": [
            {"title": "Letter I", "content": "You will rejoice to hear that no disaster has accompanied the commencement of an enterprise which you have regarded with such evil forebodings. I arrived here yesterday, and my first task is to assure my dear sister of my welfare and increasing confidence in the success of my undertaking.\n\nI am already far north of London, and as I walk in the streets of Petersburgh, I feel a cold northern breeze play upon my cheeks, which braces my nerves and fills me with delight."},
            {"title": "Chapter I", "content": "I am by birth a Genevese, and my family is one of the most distinguished of that republic. My ancestors had been for many years counsellors and syndics, and my father had filled several public situations with honour and reputation. He was respected by all who knew him for his integrity and indefatigable attention to public business. He passed his younger days perpetually occupied by the affairs of his country."},
            {"title": "Chapter II", "content": "We were brought up together; there was not quite a year difference in our ages. I need not say that we were strangers to any species of disunion or dispute. Harmony was the soul of our companionship, and the diversity and contrast that subsisted in our characters drew us nearer together. Elizabeth was of a calmer and more concentrated disposition; but, with all my ardour, I was capable of a more intense application and was more deeply smitten with the thirst for knowledge."},
        ]
    },
    {
        "id": 5,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "cover_color": "#90caf9",
        "accent": "#1565c0",
        "year": 1925,
        "moods": ["melancholic", "romantic", "classic", "nostalgic"],
        "description": "Jazz Age opulence, the green light across the bay, and the elusive American Dream in Fitzgerald's golden tragedy.",
        "pages": [
            {"title": "Chapter I", "content": "In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since.\n\n\"Whenever you feel like criticizing anyone,\" he told me, \"just remember that all the people in this world haven't had the advantages that you've had.\"\n\nHe didn't say any more, but we've always been unusually communicative in a reserved way, and I understood that he meant a great deal more than that."},
            {"title": "Chapter II", "content": "About half way between West Egg and New York the motor road hastily joins the railroad and runs beside it for a quarter of a mile, so as to shrink away from a certain desolate area of land. This is a valley of ashes—a fantastic farm where ashes grow like wheat into ridges and hills and grotesque gardens; where ashes take the forms of houses and chimneys and rising smoke and, finally, with a transcendent effort, of ash-grey men who move dimly and already crumbling through the powdery air."},
        ]
    },
    {
        "id": 6,
        "title": "Moby Dick",
        "author": "Herman Melville",
        "cover_color": "#80deea",
        "accent": "#00838f",
        "year": 1851,
        "moods": ["adventurous", "philosophical", "epic", "dark"],
        "description": "Captain Ahab's all-consuming quest for the white whale drives men to the edge of obsession and the sea.",
        "pages": [
            {"title": "Chapter I – Loomings", "content": "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen and regulating the circulation.\n\nWhenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me, that it requires a strong moral principle to prevent me from deliberately stepping into the street, and methodically knocking people's hats off—then, I account it high time to get to sea as soon as I can."},
            {"title": "Chapter II – The Carpet-Bag", "content": "I stuffed a shirt or two into my old carpet-bag, tucked it under my arm, and started for Cape Horn and the Pacific. Quitting the good city of old Manhatto, I duly arrived in New Bedford. It was a Saturday night in December. Much was I disappointed upon learning that the little packet for Nantucket had already sailed, and that no way of reaching that place would offer, till the following Monday."},
        ]
    },
    {
        "id": 7,
        "title": "Jane Eyre",
        "author": "Charlotte Brontë",
        "cover_color": "#f48fb1",
        "accent": "#880e4f",
        "year": 1847,
        "moods": ["romantic", "dark", "classic", "emotional"],
        "description": "Orphaned Jane Eyre finds love, independence and haunting secrets at the brooding Thornfield Hall.",
        "pages": [
            {"title": "Chapter I", "content": "There was no possibility of taking a walk that day. We had been wandering, indeed, in the leafless shrubbery an hour in the morning; but since dinner (Mrs. Reed, when there was no company, dined early) the cold winter wind had brought with it clouds so sombre, and a rain so penetrating, that further out-door exercise was now out of the question.\n\nI was glad of it: I never liked long walks, especially on chilly afternoons: dreadful to me was the coming home in the raw twilight, with nipped fingers and toes, and a heart saddened by the chidings of Bessie, the nurse, and humbled by the consciousness of my physical inferiority to Eliza, John, and Georgiana Reed."},
            {"title": "Chapter II", "content": "I resisted all the way: a new thing for me, and a circumstance which greatly strengthened the bad opinion Bessie and Miss Abbot were disposed to entertain of me. The fact is, I was a trifle beside myself; or rather out of myself, as the French would say: I was conscious that a moment's mutiny had already rendered me liable to strange penalties, and, like any other rebel slave, I felt resolved, in my desperation, to go all lengths."},
        ]
    },
    {
        "id": 8,
        "title": "The Odyssey",
        "author": "Homer",
        "cover_color": "#ffcc80",
        "accent": "#e65100",
        "year": -800,
        "moods": ["adventurous", "epic", "classic", "mythical"],
        "description": "Odysseus's ten-year voyage home from Troy is the ultimate adventure — gods, monsters, temptation and longing.",
        "pages": [
            {"title": "Book I – Athena Inspires the Prince", "content": "Tell me, O muse, of that ingenious hero who travelled far and wide after he had sacked the famous town of Troy. Many cities did he visit, and many were the nations with whose manners and customs he was acquainted; moreover he suffered much by sea while trying to save his own life and bring his men safely home; but do what he might he could not save his men, for they perished through their own sheer folly in eating the cattle of the Sun-god Hyperion; so the god prevented them from ever reaching home."},
            {"title": "Book V – Odysseus and Calypso", "content": "Calypso, the nymph, knew him not, for the gods who live at ease had long since hidden him in her hollow caves, feeding him on ambrosia and sweet nectar, but he was looking out disconsolately over the sea as was his wont. His heart was weary with longing for his home, for Ithaca, for the smoke rising up from the chimneys of his house, for his wife, and for his son."},
        ]
    },
    {
        "id": 9,
        "title": "The Time Machine",
        "author": "H.G. Wells",
        "cover_color": "#ce93d8",
        "accent": "#6a1b9a",
        "year": 1895,
        "moods": ["curious", "adventurous", "philosophical", "thrilling"],
        "description": "An inventor hurtles 800,000 years into the future and discovers a humanity transformed beyond recognition.",
        "pages": [
            {"title": "Introduction", "content": "The Time Traveller (for so it will be convenient to speak of him) was expounding a recondite matter to us. His grey eyes shone and twinkled, and his usually pale face was flushed and animated. The fire burned brightly, and the soft radiance of the incandescent lights in the lilies of silver caught the bubbles that flashed and passed in our glasses.\n\nOur chairs, being his patents, embraced and caressed us rather than submitted to be sat upon, and there was that luxurious after-dinner atmosphere when thought roams gracefully free of the trammels of precision."},
            {"title": "Chapter II – The Machine", "content": "I do not mean to ask you to accept anything without reasonable ground for it. You will soon admit as much as I need from you. You know of course that a mathematical line, a line of thickness nil, has no real existence. They taught you that? Neither has a mathematical plane. These things are mere abstractions. So, too, a cube, having only three dimensions, cannot have a real existence."},
        ]
    },
    {
        "id": 10,
        "title": "Little Women",
        "author": "Louisa May Alcott",
        "cover_color": "#ffab91",
        "accent": "#bf360c",
        "year": 1868,
        "moods": ["heartwarming", "nostalgic", "emotional", "classic"],
        "description": "The March sisters — Meg, Jo, Beth, and Amy — grow up, dream, love, and lose in this beloved American classic.",
        "pages": [
            {"title": "Chapter I – Playing Pilgrims", "content": "\"Christmas won't be Christmas without any presents,\" grumbled Jo, lying on the rug.\n\n\"It's so dreadful to be poor!\" sighed Meg, looking down at her old dress.\n\n\"I don't think it's fair for some girls to have plenty of pretty things, and other girls nothing at all,\" added little Amy, with an injured sniff.\n\n\"We've got Father and Mother, and each other,\" said Beth contentedly from her corner."},
            {"title": "Chapter II – A Merry Christmas", "content": "Jo was the first to wake in the gray dawn of Christmas morning. No stockings hung at the fireplace, and for a moment she felt as much disappointed as she did long ago, when her little sock fell down because it was crammed so full of goodies. Then she remembered her mother's promise and, slipping her hand under her pillow, drew out a little crimson-covered book."},
        ]
    },
    # === Javyriyah Fatima Asif ===
    {
        "id": 11,
        "title": "Whispers of a Tired Soul",
        "author": "Javyriyah Fatima Asif",
        "cover_color": "#b39ddb",
        "accent": "#4527a0",
        "year": 2023,
        "moods": ["melancholic", "emotional", "introspective", "dark"],
        "description": "A deeply personal collection of prose and poetry exploring exhaustion, healing, and the quiet courage of continuing.",
        "pages": [
            {"title": "I. The Weight of Silence", "content": "There is a peculiar kind of tired that sleep cannot fix. It settles into your bones like winter — patient, thorough, unhurried. You wake and it is still there, wearing your name like a coat it borrowed and never returned.\n\nI have learned to carry it. Not because I am strong, but because the alternative is to stand still in the middle of a road, and roads do not wait for the broken-hearted.\n\nThis is not a sad story. It is just an honest one."},
            {"title": "II. Letter to Myself at 3AM", "content": "You are not falling apart. You are just feeling everything at once, and your ribcage was never designed to be a warehouse.\n\nPut something down. You are allowed.\n\nThe stars outside your window have been burning for billions of years and they still show up every night. You have been alive for far less time and you are still here, which is, by any measure, remarkable.\n\nDrink some water. Go to sleep. The morning will not fix everything, but it will be a new hour, and new hours have a way of breathing."},
            {"title": "III. On Becoming", "content": "I used to think healing was a destination. A place you arrived at, luggage-free, blinking in the good light.\n\nNow I think it is more like learning to swim. You still swallow water sometimes. You still panic when the depth surprises you. But your arms remember what to do, and that remembering is enough.\n\nI am becoming. Slowly. Imperfectly. With soil under my fingernails and wonder in my chest.\n\nI think that is more than enough."},
            {"title": "IV. The Garden in My Chest", "content": "Some days I grow wildflowers. Some days I grow weeds. Most days I cannot tell the difference until they bloom.\n\nBut I have stopped pulling everything up by the root out of fear. Some things need a season to reveal themselves. Some things just need patience and a little rain.\n\nI am learning to be a patient gardener of myself."},
        ]
    },
    {
        "id": 12,
        "title": "Between Two Rivers",
        "author": "Javyriyah Fatima Asif",
        "cover_color": "#80cbc4",
        "accent": "#004d40",
        "year": 2024,
        "moods": ["nostalgic", "philosophical", "emotional", "heartwarming"],
        "description": "A novel exploring the tension between roots and wings — a young woman caught between her heritage and her future.",
        "pages": [
            {"title": "Part One: The River That Stays", "content": "My grandmother always said that rivers know things. Not the loud, rushing kind — those are just showing off. She meant the slow ones, the ones that have been sitting in the same place for so long they have learned the names of the stones on their beds.\n\nI grew up beside one such river. It ran along the back of our village like a secret kept out in the open, and I used to press my palms flat against its surface in summer, feeling the cold move through me like a thought I hadn't had yet."},
            {"title": "Part Two: The River That Moves", "content": "The city does not have a river. It has traffic, which is a kind of current, I suppose, if you squint.\n\nI arrived on a Tuesday in September with one suitcase and my mother's voice still ringing in my ears: don't forget where you come from.\n\nI wanted to say: how could I? But I had not yet learned that forgetting is not something you choose. It happens in small ways. First you stop saying the words for things in your first language. Then you stop dreaming in it."},
            {"title": "Part Three: Finding the Delta", "content": "There is a thing that happens when two rivers meet. The water does not choose sides. It does not remember which bank it came from. It simply becomes something new — wider, deeper, slower and faster at once.\n\nI think about this often, now that I am older, now that I can look back and see the two currents of my life without flinching.\n\nI am the delta. I always was."},
        ]
    },
    {
        "id": 13,
        "title": "Of Stars and Small Things",
        "author": "Javyriyah Fatima Asif",
        "cover_color": "#fff176",
        "accent": "#f9a825",
        "year": 2022,
        "moods": ["whimsical", "heartwarming", "curious", "playful"],
        "description": "A charming collection of short stories about ordinary magic — the kind found in teacups, old letters, and late-night conversations.",
        "pages": [
            {"title": "The Teacup That Remembered", "content": "The teacup had been on the second shelf for thirty years. It had watched three generations of women stand in that kitchen — the grandmother who bought it, the daughter who forgot about it, and now the granddaughter who found it wrapped in newspaper at the back of a moving box.\n\nShe held it up to the light. It was chipped on one side, blue-and-white pattern worn almost smooth at the handle.\n\n\"Why did she keep this?\" she wondered aloud.\n\nThe answer, of course, was that some things are not kept for their usefulness. They are kept because they are witnesses."},
            {"title": "The Letter That Arrived Late", "content": "The letter arrived on a Wednesday, forty-seven years after it was sent.\n\nThe postal service offered no explanation. These things happen, they said, which is the kind of answer that explains nothing and everything at once.\n\nThe woman who opened it was eighty-one. The woman who had been meant to receive it was no longer alive. But her daughter was. And she sat at the kitchen table for a long time, reading words her mother had never read, from someone her mother had never stopped loving.\n\nSome things, it turns out, arrive exactly when they are supposed to."},
            {"title": "The Conversation at 2AM", "content": "They were not supposed to still be talking at 2AM. They had both agreed, separately and without consulting each other, that they were not the kind of people who stayed up talking anymore. They were adults now. They had things in the morning.\n\nAnd yet.\n\nThe tea had gone cold. The candle had burned to a stub. Outside, a cat was doing something complicated on the fence.\n\nShe said something she had never said out loud before, and he listened without trying to fix it, and that was perhaps the most extraordinary thing that had happened all year."},
        ]
    },
]

MOOD_KEYWORDS = {
    "happy": ["playful", "whimsical", "heartwarming"],
    "sad": ["melancholic", "emotional", "nostalgic"],
    "adventurous": ["adventurous", "thrilling", "epic"],
    "curious": ["curious", "philosophical", "clever"],
    "romantic": ["romantic", "classic", "emotional"],
    "scared": ["dark", "mysterious", "thrilling"],
    "nostalgic": ["nostalgic", "classic", "heartwarming"],
    "thoughtful": ["philosophical", "introspective", "classic"],
    "excited": ["adventurous", "playful", "curious"],
    "calm": ["whimsical", "nostalgic", "heartwarming"],
    "lonely": ["emotional", "melancholic", "introspective"],
    "inspired": ["philosophical", "epic", "curious"],
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/books")
def get_books():
    return jsonify(BOOKS)

@app.route("/api/suggest", methods=["POST"])
def suggest():
    data = request.json
    mood = data.get("mood", "").lower()
    keywords = MOOD_KEYWORDS.get(mood, [])
    
    if not keywords:
        # fuzzy match
        for key, vals in MOOD_KEYWORDS.items():
            if key in mood or mood in key:
                keywords = vals
                break
    
    scored = []
    for book in BOOKS:
        score = sum(1 for k in keywords if k in book["moods"])
        if score > 0:
            scored.append((score, book))
    
    scored.sort(key=lambda x: -x[0])
    
    if scored:
        top_score = scored[0][0]
        top_books = [b for s, b in scored if s == top_score]
        pick = random.choice(top_books)
    else:
        pick = random.choice(BOOKS)
    
    return jsonify(pick)

@app.route("/api/book/<int:book_id>")
def get_book(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
