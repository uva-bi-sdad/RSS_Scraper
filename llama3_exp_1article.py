import transformers
import torch
from tqdm import tqdm
import time

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

# Initialize the text generation pipeline
pipeline = transformers.pipeline(
    "text-generation", 
    model=model_id, 
    model_kwargs={"torch_dtype": torch.bfloat16}, 
    device_map="auto"
)

# Define the dialogs
dialogs = [
    [
        {"role": "system", "content": "Your role is that of an economist specializing in the evaluation of green product and process innovations."},
        {"role": "user", "content": "A 'green innovation' is an innovation that contributes to environmental sustainability goals."},
        {"role": "user", "content": "'Business innovation' is defined as a new or improved product or business process (or combination thereof) that differs significantly from the firm's previous products or business processes and that has been introduced on the market or brought into use by the firm."},
        {"role": "user", "content": "'Business product innovation' is defined as a new or improved good or service that differs significantly from the firm’s previous goods or services and that has been introduced on the market. This includes quality, technical specifications, reliability, durability, economic efficiency during use, affordability, convenience, usability, and user friendliness."},
        {"role": "user", "content": "'Business process innovation' is a new or improved business process for one or more business functions that differs significantly from the firm’s previous business processes and that has been brought into use in the firm. This includes greater efficacy, resource efficiency, reliability and resilience, affordability, convenience, and usability. Business functions include production methods; distribution and logistics; information and communication systems; marketing methods; and administration and management activities. The implementation of business process innovations is often tied to the adoption and modification of digital technologies."},
        {"role": "user", "content": "A 'green product' can be defined comprehensively as any good or service that is designed, manufactured, and used in a way that significantly reduces its environmental impact throughout its life cycle. This encompasses the use of environmentally benign materials, sustainable production processes that minimize energy consumption and waste, and product functionalities that support recycling and low environmental impact during usage and disposal. Green products also strive to conserve natural resources and reduce the use of toxic substances, thereby enhancing or protecting the environment while promoting both ecological and human health benefits."},
        {"role": "user", "content": "A 'green process' refers to a method or technique in manufacturing, production, or any other operational activity that minimizes environmental impacts and promotes sustainability. These processes aim to reduce waste, conserve natural resources, decrease energy consumption, and limit the release of harmful substances into the environment. Green processes often involve using renewable resources, recycling materials, employing energy-efficient technologies, and ensuring that products are biodegradable or easily recyclable at the end of their life cycle."},
        {"role": "user", "content": "'Greenwashing' is the act of making false or misleading statements about the environmental benefits of a product or practice. This deceptive marketing tactic involves the dissemination of misleading or false information to give the impression that a company's products, aims, or policies are environmentally responsible when this may not be the case. Greenwashing can manifest in various forms, such as through advertising, public statements, eco-labeling, or packaging that suggests environmental benefits which are unsubstantiated or exaggerated."}, 
        {"role": "user", "content": "article text: \"Last year, I became obsessed with a plastic cup. It was a small container that held diced fruit, the type thrown into lunch boxes. And it was the first product I\u2019d seen born of what\u2019s being touted as a cure for a crisis. Plastic doesn\u2019t break down in nature. If you turned all of what\u2019s been made into cling wrap, it would cover every inch of the globe. It\u2019s piling up, leaching into our water and poisoning our bodies. Scientists say the key to fixing this is to make less of it; the world churns out 430 million metric tons each year. But businesses that rely on plastic production, like fossil fuel and chemical companies, have worked since the 1980s to spin the pollution as a failure of waste management \u2014 one that can be solved with recycling. Industry leaders knew then what we know now: Traditional recycling would barely put a dent in the trash heap. It\u2019s hard to transform flimsy candy wrappers into sandwich bags, or to make containers that once held motor oil clean enough for milk. Now, the industry is heralding nothing short of a miracle: an \u201cadvanced\u201dtype of recycling known as pyrolysis \u2014 \u201cpyro\u201d means fire and \u201clysis\u201d means separation. It uses heat to break plastic all the way down to its molecular building blocks. While old-school, \u201cmechanical\u201d recycling yields plastic that\u2019s degraded or contaminated, this type of \u201cchemical\u201d recycling promises plastic that behaves like it\u2019s new, and could usher in what the industry casts as a green revolution: Not only would it save hard-to-recycle plastics like frozen food wrappers from the dumpster, but it would turn them into new products that can replace the old ones and be chemically recycled again and again. So when three companies used ExxonMobil\u2019s pyrolysis-based technology to successfully conjure up that fruit cup, they announced it to the world. \u201cThis is a significant milestone,\u201d said Printpack, which turned the plastic into cups. The fruit supplier Pacific Coast Producers called it \u201cthe most important initiative a consumer-packaged goods company can pursue.\u201d \u201cExxonMobil is supporting the circularity of plastics,\u201d the August 2023 news release said, citing a buzzword that implies an infinite loop of using, recycling and reusing. They were so proud, I hoped they would tell me all about how they made the cup, how many of them existed and where I could buy one. Let\u2019s take a closer look at that Printpack press release, which uses convoluted terms to describe the recycled plastic in that fruit cup: \u201c30% ISCC PLUS certified-circular\u201d \u201cmass balance free attribution\u201d It\u2019s easy to conclude the cup was made with 30% recycled plastic \u2014 until you break down the numerical sleight of hand that props up that number. It took interviews with a dozen academics, consultants, environmentalists and engineers to help me do just that. Stick with me as I unravel it all. So began my long \u2014 and, well, circular \u2014 pursuit of the truth at a time when it really matters. This year, nearly all of the world\u2019s countries are hammering out a United Nations treaty to deal with the plastic crisis. As they consider limiting production, the industry is making a hard push to shift the conversation to the wonders of chemical recycling. It\u2019s also buying ads during cable news shows as U.S. states consider laws to limit plastic packaging and lobbying federal agencies to loosen the very definition of what it means to recycle. It\u2019s \u201cvery, very, very, very difficult\u201d to break down plastic that way. It\u2019s been selling governments on chemical recycling, with quite a bit of success. American and European regulatorshave spent tens of millions subsidizing pyrolysis facilities. Half of all U.S. states have eased air pollution rules for the process, which has been found to release carcinogens like benzene and dioxins and give off more greenhouse gases than making plastic from crude oil. Given the high stakes of this moment, I set out to understand exactly what the world is getting out of this recycling technology. For months, I tracked press releases, interviewed experts, tried to buy plastic made via pyrolysis and learned more than I ever wanted to know about the science of recycled molecules. Under all the math and engineering, I found an inconvenient truth: Not much is being recycled at all, nor is pyrolysis capable of curbing the plastic crisis. Not now. Maybe not ever. In traditional recycling, plastic is turned into tiny pellets or flakes, which you can melt again and mold back into recycled plastic products. Even in a real-life scenario, where bottles have labels and a little bit of juice left in them, most of the plastic products that go into the process find new life. The numbers are much lower for pyrolysis. It\u2019s \u201cvery, very, very, very difficult\u201d to break down plastic that way, said Steve Jenkins, vice president of chemicals consulting at Wood Mackenzie, an energy and resources analytics firm. \u201cThe laws of nature and the laws of physics are trying to stop you.\u201d Waste is heated until it turns into oil. Part of that oil is composed of a liquid called naphtha, which is essential for making plastic. There are two ingredients in the naphtha that recyclers want to isolate: propylene and ethylene \u2014 gases that can be turned into solid plastics. To split the naphtha into different chemicals, it\u2019s fed into a machine called a steam cracker. Less than half of what it spits out becomes propylene and ethylene. This means that if a pyrolysis operator started with 100 pounds of plastic waste, it can expect to end up with 15-20 pounds of reusable plastic. Experts told me the process can yield less if the plastic used is dirty or more if the technology is particularly advanced. I reached out to several companies to ask how much new plastic their processes actually yield, and none provided numbers. The American Chemistry Council, the nation\u2019s largest plastic lobby, told me that because so many factors impact a company\u2019s yield, it\u2019s impossible to estimate that number for the entire industry. With mechanical recycling, it\u2019s hard to make plastic that\u2019s 100% recycled; it\u2019s expensive to do, and the process degrades plastic. Recycled pellets are often combined with new pellets to make stuff that\u2019s 25% or 50% recycled, for example. But far less recycled plastic winds up in products made through pyrolysis. That\u2019s because the naphtha created using recycled plastic is contaminated. Manufacturers add all kinds of chemicals to make products bend or keep them from degrading in the sun. Recyclers can overpower them by heavily diluting the recycled naphtha. With what, you ask? Nonrecycled naphtha made from ordinary crude oil! This is the quiet \u2014 and convenient \u2014 part of the industry\u2019s revolutionary pyrolysis method: It relies heavily on extracting fossil fuels. At least 90% of the naphtha used in pyrolysis is fossil fuel naphtha. Only then can it be poured into the steam cracker to separate the chemicals that make plastic. So at the end of the day, nothing that comes out of pyrolysis physically contains more than 10% recycled material (though experts and studies have shown that, in practice, it\u2019s more like 5% or 2%). Ten percent doesn\u2019t look very impressive. Some consumers are willing to pay a premium for sustainability, so companies use a form of accounting called mass balance to inflate the recycled-ness of their products. It\u2019s not unlike offset schemes I\u2019ve uncovered that absolve refineries of their carbon emissions and enable mining companies to kill chimpanzees. Industry-affiliated groups like the International Sustainability and Carbon Certification write the rules. (ISCC didn\u2019t respond to requests for comment.) Legislation in the European Union already forbids free attribution, and leaders are debating whether to allow other forms of mass balance. To see how this works, let\u2019s take a look at what might happen to a batch of recycled naphtha. Let\u2019s say the steam cracker splits the batch into 100 pounds of assorted ingredients. There are many flavors of this kind of accounting. Another version of free attribution would allow the company to take that entire 30-pound batch of \u201c33% recycled\u201d pouches and split them even further: A third of them, 10 pounds, could be labeled 100% recycled \u2014 shifting the value of the full batch onto them \u2014 so long as the remaining 20 pounds aren\u2019t labeled as recycled at all. As long as you avoid double counting, Jenkins told me, you can attribute the full value of recycled naphtha to the products that will make the most money. Companies need that financial incentive to recoup the costs of pyrolysis, he said. But it\u2019s hard to argue that this type of marketing is transparent. Consumers aren\u2019t going to parse through the caveats of a 33% recycled claim or understand how the green technology they\u2019re being sold perpetuates the fossil fuel industry. I posed the critiques to the industry, including environmentalists\u2019 accusations that mass balance is just a fancy way of greenwashing. The American Chemistry Council told me it\u2019s impossible to know whether a particular ethylene molecule comes from pyrolysis naphtha or fossil fuel naphtha; the compounds produced are \u201cfungible\u201d and can be used for multiple products, like making rubber, solvents and paints that would reduce the amount of new fossil fuels needed. Its statement called mass balance a \u201cwell-known methodology\u201d that\u2019s been used by other industries including fair trade coffee, chocolate and renewable energy. Legislation in the European Union already forbids free attribution, and leaders are debating whether to allow other forms of mass balance. U.S. regulation is far behind that, but as the Federal Trade Commission revises its general guidelines for green marketing, the industry is arguing that mass balance is crucial to the future of advanced recycling. \u201cThe science of advanced recycling simply does not support any other approach because the ability to track individual molecules does not readily exist,\u201d said a comment from ExxonMobil. If you think navigating the ins and outs of pyrolysis is hard, try getting your hands on actual plastic made through it. It\u2019s not as easy as going to the grocery store. Those water bottles you might see with 100% recycled claims are almost certainly made through traditional recycling. The biggest giveaway is that the labels don\u2019t contain the asterisks or fine print typical of products made through pyrolysis, like \u201cmass balance,\u201d \u201ccircular\u201d or \u201ccertified.\u201d When I asked about the fruit cup, ExxonMobil directed me to its partners. Printpack didn\u2019t respond to my inquiries. Pacific Coast Producers told me it was \u201cengaged in a small pilot pack of plastic bowls that contain post-consumer content with materials certified\u201d by third parties, and that it \u201chas made no label claims regarding these cups and is evaluating their use.\u201d I pressed the American Chemistry Council for other examples. \u201cChemical recycling is a proven technology that is already manufacturing products, conserving natural resources, and offering the potential to dramatically improve recycling rates,\u201d said Matthew Kastner, a media relations director. His colleague added that much of the plastic made via pyrolysis is \u201cbeing used for food- and medical-grade packaging, oftentimes not branded.\u201d They provided links to products including a Chevron Phillips Chemical announcement about bringing recycled plastic food wrapping to retail stores. \u201cFor competitive reasons,\u201d a Chevron spokesperson declined to discuss brand names, the product\u2019s availability or the amount produced. In another case, a grocery store chain sold chicken wrapped in plastic made by ExxonMobil\u2019s pyrolysis process. The producers told me they were part of a small project that\u2019s now discontinued. In the end, I ran down half a dozen claims about products that came out of pyrolysis; each either existed in limited quantities or had its recycled-ness obscured with mass balance caveats. Then this April, nearly eight months after I\u2019d begun my pursuit, I could barely contain myself when I got my hands on an actual product. I was at a United Nations treaty negotiation in Ottawa, Ontario, and an industry group had set up a nearby showcase. On display was a case of Heinz baked beans, packaged in \u201c39% recycled plastic*.\u201d (The asterisk took me down an online rabbit hole about certification and circularity. Heinz didn\u2019t respond to my questions.) This, too, was part of an old trial. The beans were expired. Pyrolysis is a \u201cfairy tale,\u201d I heard from Neil Tangri, the science and policy director at the environmental justice network Global Alliance for Incinerator Alternatives. He said he\u2019s been hearing pyrolysis claims since the \u201990s but has yet to see proof it works as promised. \u201cIf anyone has cracked the code for a large-scale, efficient and profitable way to turn plastic into plastic,\u201d he said, \u201cevery reporter in the world\u201d would get a tour. If I did get a tour, I wondered, would I even see all of that stubborn, dirty plastic they were supposedly recycling? The industry\u2019s marketing implied we could soon toss sandwich bags and string cheese wrappers into curbside recycling bins, where they would be diverted to pyrolysis plants. But I grew skeptical as I watched a webinar for ExxonMobil\u2019s pyrolysis-based technology, the kind used to make the fruit cup. The company showed photos of plastic packaging and oil field equipment as examples of its starting material but then mentioned something that made me sit up straight: It was using pre-consumer plastic to \u201cgive consistency\u201d to the waste stream. Chemical plants need consistency, so it\u2019s easier to use plastic that hasn\u2019t been gunked up by consumer use, Jenkins explained. But plastic waste that had never been touched by consumers, such as industrial scrap found at the edges of factory molds, could easily be recycled the old-fashioned way. Didn\u2019t that negate the need for this more polluting, less efficient process? I asked ExxonMobil how much post-consumer plastic it was actually using. Catie Tuley, a media relations adviser, said it depends on what\u2019s available. \u201cAt the end of the day, advanced recycling allows us to divert plastic waste from landfills and give new life to plastic waste.\u201d I posed the same question to several other operators. A company in Europe told me it uses \u201cmixed post-consumer, flexible plastic waste\u201d and does not recycle pre-consumer waste. But this spring at an environmental journalism conference, an American Chemistry Council executive confirmed the industry\u2019s preference for clean plastic as he talked about an Atlanta-based company and its pyrolysis process. My colleague Sharon Lerner asked whether it was sourcing curbside-recycled plastic for pyrolysis. If Nexus Circular had a \u201cmagic wand,\u201d it would, he acknowledged, but right now that kind of waste \u201cisn\u2019t good enough.\u201d He added, \u201cIt\u2019s got tomatoes in it.\u201d (Nexus later confirmed that most of the plastic it used was pre-consumer and about a third was post-consumer, including motor oil containers sourced from car repair shops and bags dropped off at special recycling centers.) Clean, well-sorted plastic is a valuable commodity. If the chemical recycling industry grows, experts told me, those companies could end up competing with the far more efficient traditional recycling. To spur that growth, the American Chemistry Council is lobbying for mandates that would require more recycled plastic in packaging; it wants to make sure that chemically recycled plastic counts. \u201cThis would create market-driven demand signals,\u201d Kastner told me, and ease the way for large-scale investment in new chemical recycling plants. I asked Jenkins, the energy industry analyst, to play out this scenario on a larger scale. Were all of these projects adding up? Could the industry conceivably make enough propylene and ethylene through pyrolysis to replace much of our demand for new plastic? He looked three years into the future, using his company\u2019s latest figures on global pyrolysis investment, and gave an optimistic assessment. At best, the world could replace 0.2% of new plastic churned out in a year with products made through pyrolysis. ProPublica is a Pulitzer Prize-winning investigative newsroom. Sign up for The Big Story newsletter to receive stories like this one in your inbox.\""},
        {"role": "user", "content": "If the article satisfies the definitions of green innovation, respond with the phrase: 'TRUE' and the reason why this is green innovation. If not, respond with the phrase 'FALSE' and the reason why this is not green innovation. Label this text 'green_innovation'."},
        {"role": "user", "content": "If the article talks about a good or service that meets the definition of business product innovation, respond with the phrase 'TRUE' and the reason why it is a business product innovation. If not, respond with the phrase 'FALSE' and the reason why this is not a business product innovation. Label this text 'business_product_innovation'."},
        {"role": "user", "content": "If the article talks about a production or delivery method that meets the definition of business process innovation, respond with the phrase 'TRUE' and the reason why this is a business process innovation. If not, respond with the phrase 'FALSE' and the reason why this is not a business process innovation. Label this text 'business_process_innovation'."},
        {"role": "user", "content": "If the article talks about a good or service that meets the definition of a green product, respond with the phrase 'TRUE' and the reason why it is a green product. If not, respond with the phrase 'FALSE' and the reason why this is not a green product. Label this text 'green_product'."},
        {"role": "user", "content": "If the article talks about a good or service that meets the definition of a green process, respond with the phrase 'TRUE' and the reason why it is a green process. If not, respond with the phrase 'FALSE' and the reason why this is not a green process. Label this text 'green_process'."},
        {"role": "user", "content": "If the company is identified, search the internet for all references to the company and respond with the most likely official name of the company. Label this text 'official_company_name'."},
        {"role": "user", "content": "If the product or process is named, respond with the product or process name, otherwise respond 'product or process not identified'. Label this text 'product_or_process'."},
        {"role": "user", "content": "How would you categorize this innovation using the North American Industry Classification System (NAICS)? Respond with 'Likely NAICS Codes: ' and the two most likely categories and codes. Label this text 'likely_naics_codes'."},
        {"role": "user", "content": "Respond whether or not you think the article text describing the product or process innovation is an example of greenwashing and why you answered this way. Label this text 'greenwashing'."},
        {"role": "user", "content": "Summarize the article text in 4 sentences or less. Label this text 'summary'."}
    ]
]

# Iterate through the dialogs and generate responses
for dialog in dialogs:
    conversation = ""
    for turn in dialog:
        role = turn["role"]
        content = turn["content"]
        if role == "system":
            conversation += f"[{content}]\n"
        else:
            conversation += f"{role.capitalize()}: {content}\n"
    
    # Generate a response for the user prompt
    response = pipeline(conversation, max_new_tokens=1000, do_sample=True, temperature=0.7, top_p=0.9)
    
    # Extract and print the generated response
    generated_text = response[0]['generated_text'].strip()
    print(f"Conversation:\n{conversation}")
    print(f"Generated Response:\n{generated_text}")
    print("\n==================================\n")
