# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions
import scrape as houseData


class MyBot(ActivityHandler):
	"""
	This bot will respond to the user's input with suggested actions.
	Suggested actions enable your bot to present buttons that the user
	can tap to provide input.
	"""
	houseData.getHousing()


	async def on_members_added_activity(
		self, members_added: [ChannelAccount], turn_context: TurnContext
	):
		"""
		Send a welcome message to the user and tell them what actions they may perform to use this bot
		"""

		return await self._send_welcome_message(turn_context)

	async def on_message_activity(self, turn_context: TurnContext):
		"""
		Respond to the users choice and display the suggested actions again.
		"""

		text = turn_context.activity.text.lower()
		response_text = self._process_input(text,0)

		await turn_context.send_activity(MessageFactory.text(response_text))

		return await self._send_suggested_actions(turn_context)

	async def _send_welcome_message(self, turn_context: TurnContext):
		for member in turn_context.activity.members_added:
			if member.id != turn_context.activity.recipient.id:
				await turn_context.send_activity(
					MessageFactory.text(
						"Hello and Welcome!"
					)
				)

				await self._send_suggested_actions(turn_context)

	async def _process_input(self, text: str, num: int):

		if text == "housing":
			numPosts = num + 3

			while num <= numPosts:
				await turn_context.send_activity(MessageFactory.text( "a" ))
				num += 1

		return

		if text == "resources":
			return f"do Resources"

		return "Please select a valid option from the provided choices"

	async def _send_suggested_actions(self, turn_context: TurnContext):
		"""
		Creates and sends an activity with suggested actions to the user. When the user
		clicks one of the buttons the text value from the "CardAction" will be displayed
		in the channel just as if the user entered the text. There are multiple
		"ActionTypes" that may be used for different situations.
		"""

		reply = MessageFactory.text("What are you interested in?")

		reply.suggested_actions = SuggestedActions(
			actions=[
				CardAction(
					title="Housing",
					type=ActionTypes.im_back,
					value="Housing",
				),
				CardAction(
					title="Resources",
					type=ActionTypes.im_back,
					value="Resources",
				),
			]
		)

		return await turn_context.send_activity(reply)
