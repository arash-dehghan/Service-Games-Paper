# Service Games Article and Code

This is the code and paper for an article submitted for review to Mathematics Magazine. This work is building upon the paper 'Catch-Up: A Rule That Makes Service Sports More Competitive' published in American Mathematical Monthly. This work is programmed both in Python and VBA. The abstract for the paper is as follows:

The recent work of Brams, Ismail, Kilgour, and Stromquist [?](hereinafter,BIKS) drew attention to a class of contests with interesting features. A service sport is a two- sided competition that involves rallies in which one player (or team), called the server, hits some object, usually a ball, and the receiving player attempts to return it. The back-and-forth rally ends if the serve fails or, if it is successful, as soon as a return fails. Broadly speaking, service sports include tennis, table tennis, racquetball, squash, badminton, and volleyball.
Under the most common scoring rule, the opponent of the player whose serve or return fails scores one point. For most service sports, points accumulate and the winner of the game is the first player who attains some fixed number of points, often 11 or 21. In typical service sports it is an advantage to serve, in that the server is more likely to win the point when the competitors are equally skilled. Note that we do not consider tennis because of its unique system (game, set, and match) for determining winners, and because it allows missed serves to be repeated once [?].
In tennis and table tennis, the rules specify which player is to serve and for how long. In contrast to these fixed service rules, BIKS focused on service sports that use the
• Standard Rule (SR): The player who won the previous point is the next server.
Note that SR is a variable service rule—who serves when typically varies from game to game. BIKS also discussed three alternatives to the Standard Rule that are also variable:
• Catch-Up Rule (CR): The player who lost the previous point is the next server.
• Trailing Rule A (TRa): The player who is behind in accumulated points is the next
server. In a tie, the server is the player who was ahead in total points prior to the tie.
• Trailing Rule B (TRb): The player who is behind in accumulated points is the next
server. In a tie, the server is the player who was behind in total points prior to the tie.
CR was proposed in another context by Brams and Ismail [?]; TRa was proposed in another context by Anbarci et al. [?].
Assuming serves are independent events, BIKS calculated win probabilities and expected game lengths for these rules. Remarkably, they found that win probabilities under SR and CR are in fact identical, though the expected lengths of games are not. All three of SR, CR, and TRa are strategy-proof (or incentive-compatible)—it is never in a player’s interest to deliberately lose a serve—but TRb is not.
In this article, we introduce a new family of service rules and contribute to the analysis of its properties. In a Best-of-(2k + 1) service sport, the winner is the first player to accumulate k + 1 points. Let 1 < h ≤ k. The new service rule (based on a suggestion by Steven Brams) is
• Max-h Rule (Mh): The player who won the previous point is the next server unless that player has won h consecutive points.

Thus, if he or she continues to win, the initial server serves a maximum of h times; then the opponent, providing he or she keeps on winning, is allowed h consecutive serves, etc.
There are several reasons why the Max-h Rule is worthy of study. If h = 1 were allowed, Max-h would be identical to CR; if h = k + 1 were allowed, Max-h would be the identical to SR. Thus, because 1 < h < k + 1, Max-h lies “between” CR and SR, which have equal win probabilities. Does Max-h have the same win probability as SR and CR? Similarly, one anticipates that expected game length under Max-h lies between the expected lengths under CR and SR. However, CR and SR are Markovian (they depend only on the outcome of the most recent serve), whereas Max-h is not— and, thus, Max-h has something in common with the non-Markovian TR rules. In our study, we minimize the complexity of the non-Markovian rule Max-h by restricting our attention to the case h = k = 2.