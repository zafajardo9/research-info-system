import json


data = [
        ["Abalos, Karl Christian D."        , "Quantum Computing in Healthcare"                     , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"],
        ["Aquino, Rodolfo Y.  Jr."          , "Urban Green Spaces Impact on Mental Health"          , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Aribon, Mark Anthony R. III"      , "AI-Powered Language Translation Advancements"        , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Bactasa, Melanie F."              , "Renewable Energy Storage Solutions"                  , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["Baltazar, Mary Ann Micah R., CPA" , "Impact of Social Media on Adolescents"               , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognize"  , "Faculty"],
        ["Banate, Richard B., CPA"          , "Biodiversity Conservation Strategies"                , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Bernardino, Abraham Seth R."      , "Blockchain in Supply Chain Management"               , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Bernardino, Girlie F."            , "Neuroplasticity and Learning Enhancement"            , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["Bulawit, Berna A."                , "Cybersecurity in the Internet of Things"             , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"],
        ["Calingasan, Francisco S."         , "Gene Editing Ethics and Regulations"                 , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Castillo, Eleazar E."             , "Climate Change Adaptation in Coastal Cities"         , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Caturay, Norberto V., DEM"        , "Augmented Reality in Education"                      , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["Cecogo, Nieva M."                 , "Future of Autonomous Vehicles"                       , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"],
        ["Cipriano, Erwin"                  , "Human-Computer Interaction Evolution"                , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Clenuar, Ricardo H."              , "Precision Medicine and Personalized Healthcare"      , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Cruz, Mary Grace I."              , "Effects of Microplastics on Marine Life"             , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["De Leon, Celeste L."              , "Quantum Cryptography for Secure Communication"       , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"],
        ["Delmo, Elijah Paul B."            , "AI in Financial Markets Prediction"                  , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Dolorosa, Rodrigo S., DEM"        , "Sustainable Agriculture Techniques"                  , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Domingo, Keinaz"                  , "Psychological Impact of Virtual Reality"             , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["Doromal, Cherry M."               , "5G Technology and its Applications"                  , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"],
        ["Doromal, Roberto B."              , "Artificial Womb Technology"                          , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Dungca, Leah A."                  , "Biodegradable Plastics Development"                  , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Escober, Ain Gueul E."            , "Cognitive Enhancements through Brain Stimulation"    , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["Escober, Rosicar E., Ph.D."       , "Renewable Energy Integration Challenges"             , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"],
        ["Esguerra, Firmo A."               , "Social Robots for Elderly Care"                      , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Esparagoza, Cherrylyn P."         , "Health Implications of Air Pollution"                , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Estella, Zandro T."               , "Cryptocurrencies and Global Economy"                 , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["Fabela, Noel F."                  , "Ethical Implications of AI in Warfare"               , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"],
        ["Fernandez, Alma C."               , "Urbanization and Wildlife Conservation"              , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Fulleros, Richard M."             , "Biofuels as an Alternative Energy Source"            , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Fulleros, Jorgen Z."              , "Mind-Uploading and Consciousness"                    , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["Gabasa, Asuncion V."              , "Space Tourism Feasibility"                           , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"],
        ["Garcia, Maita C."                 , "Smart Cities for Sustainable Living"                 , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Gardon, Harold Q."                , "Effects of Artificial Light on Ecosystems"           , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Gatan, Leslie O."                 , "Future of Quantum Teleportation"                     , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["Gatchalian, Irynne P."            , "Technological Unemployment Concerns"                 , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"],
        ["Gulmatico, Esther S., Ph.D."      , "Nanotechnology in Medicine"                          , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Gutierrez, Jaime Jr. P."          , "Education Reformation through Gamification"          , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Isip, John Robert F."             , "Mental Health Impacts of Social Isolation"           , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["Lara, Erwin Vicman"               , "Advancements in Quantum Biology"                     , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"],
        ["Leynes, Jerome Chrstopher G."     , "Food Security in a Changing Climate"                 , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Monzon, Demelyn E. Ph.D"          , "Algorithmic Bias in AI Systems"                      , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Monzon, Kezaiah M."               , "Trends in Human Microbiome Research"                 , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["Morales, Sheryl R."               , "Virtual Currencies and Central Banks"                , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"],
        ["Odpaga, Ernesto J., Jr."          , "Cognitive Computing and Decision-Making"             , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Oliquino, Joanna Marie DC."       , "Ocean Acidification and Marine Life"                 , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Pineda, Jose Gil C."              , "AI-Generated Art and Creativity"                     , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["Roxas, Rommel Y."                 , "Advances in Fusion Energy Technology"                , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"],
        ["Servigon, Cleotilde B."           , "Aerospace Innovations for Space Exploration"         , "2019-10-09"   , "PUP Research Publication Office", "Peer Reviewed"   , "Faculty"],
        ["Soberano, Maricar O."             , "Biometrics and Privacy Concerns"                     , "2019-10-09"   , "PUP Research Publication Office", "Web of Science"  , "Faculty"],
        ["Soberano, Philip SJ."             , "Regenerative Medicine Breakthroughs"                 , "2019-10-09"   , "PUP Research Publication Office", "Scopus"          , "Faculty"],
        ["Umali, Antonius C., DPA"          , "Social Media Influence on Political Discourse"       , "2019-10-09"   , "PUP Research Publication Office", "CHED Recognized" , "Faculty"]
    ]


def convert_to_dict(row):
    return {
        "name": row[0],
        "title": row[1],
        "content": "put any sample values", 
        "abstract": "put any sample", 
        "file_path": "path/file.pdf",
        "publisher": row[3],
        "category": row[4],
        "date_publish": row[2],
    }

json_data = [convert_to_dict(row) for row in data]

json_string = json.dumps(json_data, indent=2)

print(json_string)